from fastapi import FastAPI
from app.routers import health, users
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
app.include_router(users.router)