from fastapi import FastAPI

app = FastAPI()



from api.routers.api import router

app.include_router(router)

