from fastapi import FastAPI
from pymongo import MongoClient
from src.controller import machine_controller, index_controller
import uvicorn

app = FastAPI()
# a comment only

@app.on_event("startup")
def startup_db_client():
    # use this if you want to write to the bessy server
    app.mongodb_client = MongoClient("mongodb://mongodb.bessy.de:27017/")
    # app.mongodb_client = MongoClient("mongodb://localhost:27017/") # use this if you are writing to your local machine.
    app.database = app.mongodb_client["bessyii"]


@app.on_event("shutdown")
def shutdown_db_client():
    pass
    # app.mongodb_client.close()


app.include_router(machine_controller.router, tags=["machines"], prefix="/machine")
app.include_router(index_controller.router, tags=["index"], prefix="/index")


@app.get("/healthcheck/")
def healthcheck():
    return 'Health - OK'


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
