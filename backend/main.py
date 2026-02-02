from fastapi import FastAPI
from database import Base, engine

from models import client, car, contract, order, service, spare_part, manager, master

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Автомастерская API")


@app.get("/")
def root():
    return {"status": "API работает"}
