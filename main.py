from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
import uuid
import subprocess
import os
import shutil
from script import process_url as script_process_url

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class URLItem(BaseModel):
    url: str

tasks = {}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.post("/submit-url/")
async def submit_url(url_item: URLItem, background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {"status": "processing", "content": ""}
    background_tasks.add_task(process_url, url_item.url, task_id)
    return {"task_id": task_id}

@app.get("/check-status/{task_id}")
async def check_status(task_id: str):
    return tasks.get(task_id, {"status": "not found"})

@app.get("/download/{task_id}")
async def download_file(task_id: str):
    file_path = f"output/{task_id}.zip"
    if os.path.exists(file_path):
        return FileResponse(file_path, filename=f"{task_id}.zip")
    return {"status": "not found"}

def process_url(url: str, task_id: str):
    # Call process_url from script.py with the URL and task_id
    script_process_url(url, task_id)
    
    # Ensure the output directory exists before compressing
    output_dir = f"output/{task_id}"
    if os.path.exists(output_dir):
        shutil.make_archive(output_dir, 'zip', output_dir)
        # Update task status
        tasks[task_id] = {"status": "completed", "content": f"/download/{task_id}"}
    else:
        tasks[task_id] = {"status": "failed", "content": "Output directory not found"}