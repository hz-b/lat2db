from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

from src.controller.machine_controller import router as machine_router

app = FastAPI()
app.mount("/static", StaticFiles(directory="."), name="static")
templates = Jinja2Templates(directory=".")
app.include_router(machine_router)
app.mongodb_client = MongoClient("mongodb://localhost:27017/")  # use this if you are writing to your local machine.
app.database = app.mongodb_client["bessyii"]

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/favicon.ico")
async def favicon():
    return ""

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
