import asyncio

from fastapi import FastAPI

from db.database import create_db_and_tables

app = FastAPI()



from api.routers.api import router

app.include_router(router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()