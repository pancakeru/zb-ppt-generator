import asyncio
import uuid
from pathlib import Path
from urllib.parse import quote

from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse, Response, StreamingResponse

from core.main_job import run_full_job 
from core.pptgenerator import give_date  
from typing import Optional, Dict, Any

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    html_path = Path(__file__).parent.parent / "templates" / "index.html"
    return html_path.read_text(encoding="utf-8")

@app.get("/healthz")
def health():
    return {"ok": True}

# ----------------------------
# Progress-enabled flow (SSE)
# /start -> returns job_id
# /events/{job_id} -> streams progress lines
# /download/{job_id} -> serves the PPT by job_id
# ----------------------------
# Simple in-memory store (fine for one process)
jobs: Dict[str, Dict[str, Any]] = {}  # job_id -> {"q": asyncio.Queue, "done": asyncio.Event, "ppt": bytes|None}
def _emit(job_id: str, msg: str, pct: Optional[int] = None) -> None:
    """Push 'pct|message' to client; pct can be None."""
    line = f"{'' if pct is None else pct}|{msg}"
    jobs[job_id]["q"].put_nowait(line)

async def _run(job_id: str):
    log = make_logger(job_id)
    try:
        # High-level milestones (adjust as you like)
        _emit(job_id, "Starting… / 正在启动…", 2)
        ppt_bytes = run_full_job(log=log)  # <- your prints appear on page
        jobs[job_id]["ppt"] = ppt_bytes

        _emit(job_id, "Done! Preparing download… / 完成，准备下载…", 100)
    except Exception as e:
        _emit(job_id, f"❌ Error: {e}")
    finally:
        jobs[job_id]["done"].set()

@app.post("/start")
async def start(background: BackgroundTasks):
    job_id = uuid.uuid4().hex
    jobs[job_id] = {"q": asyncio.Queue(), "done": asyncio.Event(), "ppt": None}
    background.add_task(_run, job_id)
    return {"job_id": job_id}

@app.get("/events/{job_id}")
async def events(job_id: str):
    if job_id not in jobs:
        return Response(status_code=404)

    q: asyncio.Queue = jobs[job_id]["q"]
    done: asyncio.Event = jobs[job_id]["done"]

    async def stream():
        yield "data: connected\n\n"
        while True:
            if done.is_set():
                yield "event: done\ndata: ok\n\n"
                break
            try:
                line = await asyncio.wait_for(q.get(), timeout=1.0)
                yield f"data: {line}\n\n"
            except asyncio.TimeoutError:
                yield ": keepalive\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")

@app.get("/download/{job_id}")
def download(job_id: str):
    if job_id not in jobs or jobs[job_id]["ppt"] is None:
        return Response(status_code=404)
    filename = f"25{give_date()}周报.pptx"
    cd = f'attachment; filename="weekly_report.pptx"; filename*=UTF-8\'\'{quote(filename)}'
    return Response(
        content=jobs[job_id]["ppt"],
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": cd},
    )

from typing import Optional, Dict, Any, Callable
# … your existing imports …

def make_logger(job_id: str) -> Callable[[str, Optional[int]], None]:
    """Send a message to SSE + echo to server console."""
    def _log(msg: str, pct: Optional[int] = None) -> None:
        try:
            # UI
            _emit(job_id, str(msg), pct)
        finally:
            # Console (immediate flush so you see it live)
            print(str(msg), flush=True)
    return _log