from fastapi import FastAPI

from backend.routers.client import router as client_router
from backend.routers.car import router as car_router


app = FastAPI(title="Автромастерская API")

app.include_router(client_router)
app.include_router(car_router)

