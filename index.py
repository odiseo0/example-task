from fastapi import FastAPI

from src.api.routes import api


app = FastAPI()
app.include_router(api, prefix="/metrics")


@app.get("/")
def index():
    return "Hello World"
