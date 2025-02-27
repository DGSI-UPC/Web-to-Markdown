from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
import uuid

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
    background_tasks.add_task(fetch_url_content, url_item.url, task_id)
    return {"task_id": task_id}

@app.get("/check-status/{task_id}")
async def check_status(task_id: str):
    return tasks.get(task_id, {"status": "not found"})

async def fetch_url_content(url: str, task_id: str):
    response = requests.get(url)
    tasks[task_id] = {"status": "completed", "content": response.text}
