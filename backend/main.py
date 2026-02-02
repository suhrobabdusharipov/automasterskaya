from fastapi import FastAPI
from database import Base, engine
from models import client, car, contract, order, service, spare_part, manager, master
app = FastAPI()