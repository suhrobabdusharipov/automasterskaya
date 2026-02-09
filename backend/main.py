from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from backend.routers.client import router as client_router
from backend.routers.car import router as car_router
from backend.routers.contract import router as contract_router
from backend.routers.order import router as order_router
from backend.routers.service import router as service_router
from backend.routers.spare_part import router as spare_part_router
from backend.routers.manager import router as manager_router
from backend.routers.master import router as master_router

app = FastAPI(title="Автомастерская")

app.mount("/static",StaticFiles(directory="frontend/static"),name="static")

templates = Jinja2Templates(directory="frontend/templates")

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.get("/clients")
def clients_page(request: Request):
    return templates.TemplateResponse(
        "clients/list.html",
        {"request": request}
    )

@app.get("/clients/{client_id}")
def client_detail_page(request: Request, client_id: int):
    return templates.TemplateResponse(
        "clients/detail.html",
        {"request": request, "client_id": client_id}
    )

@app.get("/cars")
def cars_page(request: Request):
    return templates.TemplateResponse(
        "cars/list.html",
        {"request": request}
    )

@app.get("/cars/{car_id}")
def car_detail_page(request: Request, car_id: int):
    return templates.TemplateResponse(
        "cars/detail.html",
        {"request": request, "car_id": car_id}
    )

@app.get("/contracts")
def contracts_page(request: Request):
    return templates.TemplateResponse(
        "contracts/list.html",
        {"request": request}
    )

@app.get("/contracts/{contract_id}")
def contract_detail_page(request: Request, contract_id: int):
    return templates.TemplateResponse(
        "contracts/detail.html",
        {"request": request, "contract_id": contract_id}
    )

@app.get("/orders")
def orders_page(request: Request):
    return templates.TemplateResponse(
        "orders/list.html",
        {"request": request}
    )

@app.get("/orders/{order_id}")
def order_detail_page(request: Request, order_id: int):
    return templates.TemplateResponse(
        "orders/detail.html",
        {"request": request, "order_id": order_id}
    )

@app.get("/reports/orders")
def orders_report(request: Request):
    return templates.TemplateResponse(
        "reports/orders.html",
        {"request": request}
    )

@app.get("/reports/statistics")
def statistics_report(request: Request):
    return templates.TemplateResponse(
        "reports/statistics.html",
        {"request": request}
    )

app.include_router(client_router)
app.include_router(car_router)
app.include_router(contract_router)
app.include_router(order_router)
app.include_router(service_router)
app.include_router(spare_part_router)
app.include_router(manager_router)
app.include_router(master_router)

