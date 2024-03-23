import sys


from fastapi.staticfiles import StaticFiles

sys.path.append('/Users/safiullahomar/lattice/lat2db')

from fastapi import FastAPI
from pymongo import MongoClient
from lat2db.controller import machine_controller, index_controller
from lat2db import mongodb_url
from lat2db.controller.machine_controller import router as machine_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

""" app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) """

app.include_router(machine_controller.router, tags=["machines"], prefix="/machine")
app.include_router(index_controller.router, tags=["index"], prefix="/index")

app.mount("/", StaticFiles(directory="../UI/build", html=True))

@app.on_event("startup")
def startup_db_client():
    # use this if you want to write to the bessy server
    # app.mongodb_client = MongoClient("mongodb://mongodb.bessy.de:27017/")
    app.mongodb_client = MongoClient(mongodb_url) # use this if you are writing to your local machine.
    app.database = app.mongodb_client["bessyii"]


@app.on_event("shutdown")
def shutdown_db_client():
    pass
    # app.mongodb_client.close()



@app.get("/healthcheck/")
def healthcheck():
    return 'Health - OK'


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
