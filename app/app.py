import asyncio
import uuid
from pathlib import Path
from urllib.parse import quote

from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse, Response, StreamingResponse

from core.main_job import run_full_job 
from core.pptgenerator import give_date  
from typing import Optional, Dict, Any
from core.util import set_progress_logger, emit

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
def make_logger(job_id: str):
    loop = asyncio.get_running_loop()
    def log(msg: str, pct: Optional[int] = None):
        line = f"{'' if pct is None else pct}|{msg}"
        loop.call_soon_threadsafe(jobs[job_id]["q"].put_nowait, line)
    return log

async def _run(job_id: str):
    log = make_logger(job_id)
    try:
        set_progress_logger(log)                     # <-- KEY LINE
        emit("Starting… / 正在启动…", 2)
        ppt_bytes = await asyncio.to_thread(run_full_job, log)  
        jobs[job_id]["ppt"] = ppt_bytes
        emit("Done! Preparing download… / 完成，准备下载…", 100)
    except Exception as e:
        emit(f"❌ Error: {e}")
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
    filename = f"25{give_date()}符文战场周报.pptx"
    cd = f'attachment; filename="weekly_report.pptx"; filename*=UTF-8\'\'{quote(filename)}'
    return Response(
        content=jobs[job_id]["ppt"],
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": cd},
    )

from typing import Optional, Dict, Any, Callable
# … your existing imports …