import asyncio
import subprocess
import time
import uvicorn
import os
from fastapi import FastAPI, Response
from fastapi import APIRouter, Body, HTTPException
from starlette.middleware.cors import CORSMiddleware

API_V1_STR: str = "/api"

app = FastAPI(
    title="Tool Set",
    docs_url=f"{API_V1_STR}/docs",
    openapi_url=f"{API_V1_STR}/openapi.json",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in (
        "http://localhost:8080", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
router = APIRouter()


@router.post("/run_shell")
async def run_shell(
    response: Response,
    command: dict = Body(default={"params": "", "connector": ""}),
):
    
    if not command.get("connector"):
        response.status_code = 400
        return HTTPException(status_code=400, detail="Please check connector")
    # >= python 3.7
    result = subprocess.run(["docker", "images"], capture_output=True)
    return {"output": result.stdout}

@router.api_route("/test", methods=["POST", "GET"])
async def run_shell(
    response: Response,
    command: dict = Body(default={"params": "", "connector": ""}),
):
    
    await asyncio.sleep(1)
    return {"output": "result.stdout"}

app.include_router(router, prefix=API_V1_STR)


if __name__ == "__main__":
    # swagger ui http://0.0.0.0:9010/api/docs#/
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=os.getenv("BACKEND_SERVER_PORT") or 9010,
        reload=True,
    )
