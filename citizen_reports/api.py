from fastapi import FastAPI, UploadFile
import shutil
from pathlib import Path

from citizen_reports.detect_blockage import detect_blockage

app = FastAPI()

UPLOAD_DIR = Path("citizen_reports/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/report")
async def report_blockage(file: UploadFile):

    path = UPLOAD_DIR / file.filename

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = detect_blockage(path)

    return {
        "message": "Report received",
        "analysis": result
    }