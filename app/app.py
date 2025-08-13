from flask import Flask, send_file
from main import main
from pptgenerator import give_date

app = Flask(__name__)

@app.route("/generate")
def generate():
    ppt_bytes = main()
    return send_file(
        ppt_bytes,
        as_attachment=True,
        download_name=f"{give_date()}周报.pptx",
        mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )