from fastapi import APIRouter
from starlette.responses import JSONResponse
from core.logger import logger

router = APIRouter()

@router.get("/healthz")
async def healthz():
    logger.info("Healthz check called")
    return JSONResponse(status_code=200, content={"status": "ok"})

@router.get("/readyz")
async def readyz():
    logger.info("Pod is ready")
    return JSONResponse(status_code=200, content={"ready": True})