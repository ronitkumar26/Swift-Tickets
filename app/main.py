# app/main.py

import logging
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

# Routers
from app.routers import health, users, auth, ticket

# -------------------------------
# Logging configuration
# -------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------------------------------
# Initialize FastAPI
# -------------------------------
app = FastAPI(
    title="SwiftTicket API",
    description="Internal company support ticketing system",
    version="1.0.0"
)

# -------------------------------
# Middleware
# -------------------------------

# 1️. Logging Middleware: logs every request
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logging.info(
            f"{request.method} {request.url} completed in {process_time:.3f}s "
            f"status={response.status_code}"
        )
        return response

app.add_middleware(LoggingMiddleware)

# 2. Optional CORS Middleware: will enable when frontend uses a different origin

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Startup / Shutdown events
# -------------------------------
@app.on_event("startup")
async def startup_event():
    logging.info("🚀 SwiftTicket API is starting...")

@app.on_event("shutdown")
async def shutdown_event():
    logging.info("🛑 SwiftTicket API is shutting down...")

# -------------------------------
# Root route
# -------------------------------
@app.get("/")
async def root():
    return {"message": "SwiftTicket API is running"}

# -------------------------------
# Include Routers
# -------------------------------
app.include_router(health.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(ticket.router)
