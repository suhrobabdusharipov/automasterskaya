from fastapi import FastAPI

from backend.routers.client import router as client_router
from backend.routers.car import router as car_router
from backend.routers.contract import router as contract_router
from backend.routers.order import router as order_router


app = FastAPI(title="Автромастерская API")

app.include_router(client_router)
app.include_router(car_router)
app.include_router(contract_router)
app.include_router(order_router)

