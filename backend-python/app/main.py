from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Backend con Python"}