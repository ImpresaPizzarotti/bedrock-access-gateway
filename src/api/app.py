import logging
import os

import uvicorn, os
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from mangum import Mangum

from api.routers import chat, embeddings, model
from api.setting import API_ROUTE_PREFIX, DESCRIPTION, SUMMARY, TITLE, VERSION, LOG_LEVEL

config = {
    "title": TITLE,
    "description": DESCRIPTION,
    "summary": SUMMARY,
    "version": VERSION,
}

# Set logging level base on LOG_LEVEL var
logging.basicConfig(
    # level=logging.INFO,
    level = LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
app = FastAPI(**config)

allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*")
origins_list = [origin.strip() for origin in allowed_origins.split(",")] if allowed_origins != "*" else ["*"]

# Warn if CORS allows all origins
if origins_list == ["*"]:
    logging.warning("CORS is configured to allow all origins (*). Set ALLOWED_ORIGINS environment variable to restrict access.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins_list,  # nosec - configurable via ALLOWED_ORIGINS env var
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(model.router, prefix=API_ROUTE_PREFIX)
app.include_router(chat.router, prefix=API_ROUTE_PREFIX)
app.include_router(embeddings.router, prefix=API_ROUTE_PREFIX)


@app.get("/health")
async def health():
    """For health check if needed"""
    return {"status": "OK"}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger = logging.getLogger(__name__)
    
    # Log essential info only - avoid sensitive data and performance overhead
    logger.warning(
        "Request validation failed: %s %s - %s", 
        request.method, 
        request.url.path,
        str(exc).split('\n')[0]  # First line only
    )
    
    return PlainTextResponse(str(exc), status_code=400)


handler = Mangum(app)

if __name__ == "__main__":
    port: int = int(os.getenv("PORT", "8080"))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False)
