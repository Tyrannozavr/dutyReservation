from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from db.database import create_db_and_tables

app = FastAPI(docs_url="/api/docs")

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
    create_db_and_tables()
