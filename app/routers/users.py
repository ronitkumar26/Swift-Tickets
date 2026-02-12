from fastapi import APIRouter,  Depends, status, HTTPException
from app.database.sessions import Session , get_db
from app import models,  schemas

router = APIRouter(
    prefix='/users',
    tags=["users"]
)

@router.get("/", status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    users_data = db.query(models.User).all()
    return {'All Users': users_data}

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(data: schemas.user.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"Data": new_user, "message": "User created successfully!"}

@router.get("/{Id}")
def get_user_by_id(Id: int, db: Session = Depends(get_db)):
    user_id = db.query(models.User).filter(models.User.id == Id).first()
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {'User Id': user_id}

@router.put("/{Id}", status_code=status.HTTP_200_OK)
def update_user_by_id(Id: int, data: schemas.user.UserUpdate, db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.id == Id)
    user = query.first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"User with id {Id} not found")
    update_data = data.model_dump(exclude_unset=True)
    query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(user)
    print("--- User Updated Successfully ---")
    print(f"ID: {user.id}")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Password: {user.hashed_password}")
    print("---------------------------------")

    return {
        "data": user,
        "message": f"User {Id} has been updated."
    }

@router.delete("/{Id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(Id: int, db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.id == Id)
    user = query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {Id} not found")
    query.delete(synchronize_session=False)
    db.commit()
    return {"message": f"User {id} has been deleted successfully."}
    