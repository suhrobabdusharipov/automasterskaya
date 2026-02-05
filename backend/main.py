from fastapi import FastAPI

from backend.routers.client import router as client_router


app = FastAPI(title="Автомастерская API")

app.include_router(client_router)
