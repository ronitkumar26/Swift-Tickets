from fastapi import APIRouter,  Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.database.sessions import Session , get_db
from app import models,  schemas, core
from app.core.security import verify_password
from app.core import oauth2


router = APIRouter(
    prefix="/login",
    tags=["Autharization"]
)


@router.post("/")
def login(user_credentails: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentails.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    if not core.security.verify_password(user_credentails.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id, "role": user.role })
    print(access_token)

    
    return {
    "access_token": access_token, 
    "token_type": "bearer",
    "message": "Login successful"
}