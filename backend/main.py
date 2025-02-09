from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from logger import logger

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc")

from api.routers.api import router

app.include_router(router, prefix="/api")


origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=30
)


@app.on_event("startup")
def on_startup():
    logger.info("Started up")
