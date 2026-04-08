from fastapi import FastAPI
from app.routes import product_routes
import psycopg2
import os

app = FastAPI()

app.include_router(product_routes.router)

@app.get("/")
def read_root():
    return {"message": "Backend con Python"}