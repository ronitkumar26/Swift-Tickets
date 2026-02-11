from fastapi import FastAPI

app = FastAPI(
    title="SwiftTicket API",
    description="Internal company support ticketing system",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "SwiftTicket API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}