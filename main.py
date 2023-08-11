from fastapi import FastAPI
from routers.nasa_images import router

app = FastAPI()

app.include_router(router)



