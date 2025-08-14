from fastapi import FastAPI, Response
from core.main_job import run_full_job
from core.pptgenerator import give_date

app = FastAPI()

@app.get("/healthz")
def health():
    return {"ok": True}

@app.get("/report")
def report():
    ppt_bytes = run_full_job()
    filename = f"25{give_date()}.pptx"
    return Response(
        content=ppt_bytes,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )