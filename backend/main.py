from fastapi import FastAPI

from backend.routers.client import router as client_router
from backend.routers.car import router as car_router
from backend.routers.contract import router as contract_router
from backend.routers.order import router as order_router
from backend.routers.service import router as service_router
from backend.routers.spare_part import router as spare_part_router
from backend.routers.manager import router as manager_router


app = FastAPI(title="Автромастерская API")

app.include_router(client_router)
app.include_router(car_router)
app.include_router(contract_router)
app.include_router(order_router)
app.include_router(service_router)
app.include_router(spare_part_router)
app.include_router(manager_router)

