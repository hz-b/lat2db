from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import HTMLResponse, FileResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return FileResponse("src/templates/index.html")
