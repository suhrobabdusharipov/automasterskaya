from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from backend.database import engine, Base, get_db
from backend.routers import (
    car,
    client,
    contract,
    manager,
    master,
    order,
    service,
    spare_part,
    reports
)

app = FastAPI(title="Автомастерская")

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

app.include_router(car.router)
app.include_router(client.router)
app.include_router(contract.router)
app.include_router(manager.router)
app.include_router(master.router)
app.include_router(order.router)
app.include_router(service.router)
app.include_router(spare_part.router)
app.include_router(reports.router)

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        "base.html",
        {"request": request}
    )
