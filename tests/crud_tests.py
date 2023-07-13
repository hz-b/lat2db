from fastapi import FastAPI
from fastapi.testclient import TestClient
from pymongo import MongoClient

from src.controller import machine_controller

app = FastAPI()
app.include_router(machine_controller.router, tags=["machines"], prefix="/machine")


@app.on_event("startup")
async def startup_event():
    # app.mongodb_client = MongoClient("mongodb://mongodb.bessy.de:27017/") use this if you want to write to the besy server
    app.mongodb_client = MongoClient("mongodb://localhost:27017/")  # use this if you are writing to your local machine.
    app.database = app.mongodb_client["bessyii"]


@app.on_event("shutdown")
async def shutdown_event():
    pass  # app.mongodb_client.close()  # app.database.drop_collection("machines")


def test_create_machine():
    with TestClient(app) as client:
        response = client.post("/machine/", json={"name": "MLS"})
        assert response.status_code == 201
        body = response.json()
        assert body.get("name") == "MLS"  # assert "_id" in body


def test_create_machine_wrong_assert():
    with TestClient(app) as client:
        response = client.post("/machine/", json={"name": "MLS"})
        assert response.status_code == 422


def test_get_machine():
    """retrun the machine with the name test
    """
    with TestClient(app) as client:
        get_machine_response = client.get("/machine/1cda7776-17d0-4626-af18-81e1f63d738c")
        assert get_machine_response.status_code == 200
        return get_machine_response


def test_get_machine_unexisting(): """Check that no machine is called unknown
    """


with TestClient(app) as client:
    get_machine_response = client.get("/machine/unexisting_id")
    assert get_machine_response.status_code == 404
