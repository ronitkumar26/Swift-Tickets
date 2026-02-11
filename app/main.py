from fastapi import FastAPI
import psycopg2
from app.routers import health
from app.database.sessions import engine

app = FastAPI(
    title="SwiftTicket API",
    description="Internal company support ticketing system",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "SwiftTicket API is running"}

app.include_router(health.router)