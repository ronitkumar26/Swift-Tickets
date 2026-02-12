from fastapi import APIRouter,  Depends, status, HTTPException
from app.database.sessions import Session , get_db
from app import models,  schema

router = APIRouter(
    prefix='/users',
    tags=["users"]
)

@router.get("/", status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    users_data = db.query(models.User).all()
    return {'All Users': users_data}

# @router.post("/", status_code=status.HTTP_201_CREATED)
# def create_user():