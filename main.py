from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
from script import crawl
import shutil
from fastapi.responses import FileResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class URLItem(BaseModel):
    url: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.post("/submit-url/")
async def submit_url(url_item: URLItem):
    print(url_item.url)
    crawl(url_item.url)
    # Compress the markdown_output folder into a zip file
    shutil.make_archive("markdown_output", "zip", "markdown_output")

    # Return the zip file as a response
    return FileResponse("markdown_output.zip", media_type="application/zip", filename="markdown_output.zip")
