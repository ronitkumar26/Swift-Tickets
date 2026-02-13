from fastapi import FastAPI, Depends
from app.routers import health, users, auth, ticket
from app.database.sessions import engine
# from app.schemas.user import TokenData
# from app.core import oauth2

app = FastAPI(
    title="SwiftTicket API",
    description="Internal company support ticketing system",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "SwiftTicket API is running"}

# @app.get("/test-token")
# def test_token(current_user: TokenData = Depends(oauth2.get_current_user)):
#     return {"id": current_user.id, "role": current_user.role}

app.include_router(ticket.router)
app.include_router(health.router)
app.include_router(users.router)
app.include_router(auth.router)