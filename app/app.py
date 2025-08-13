from fastapi import FastAPI, Response
from core.main_job import run_full_job
from core.pptgenerator import give_date

app = FastAPI()

@app.get("/healthz")
def health():
    return {"ok": True}

@app.post("/report")
def report():
    ppt_bytes = run_full_job()
    return Response(
        content=ppt_bytes,
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        headers={"Content-Disposition": 'attachment; filename=f"{give_date()}周报.pptx"'}
    )