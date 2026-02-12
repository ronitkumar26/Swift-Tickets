from fastapi import APIRouter,  Depends, status, HTTPException
from app.database.sessions import Session , get_db
from app import models,  schemas, core
from app.core.security import hash_password
from app.core import oauth2
from app.core.oauth2 import get_current_admin
from app.schemas.user import TokenData

router = APIRouter(
    prefix='/users',
    tags=["users"]
)

# Get User

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.user.UserResponse])
def get_users(db: Session = Depends(get_db), current_admin: str = Depends(oauth2.get_current_admin)):
    users_data = db.query(models.User).all()
    return users_data

# Create User

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.user.UserResponse)
def create_user(data: schemas.user.UserCreate, db: Session = Depends(get_db)):

    hashed_password = core.security.hash_password(data.password)

    user_data = data.model_dump(exclude={"password"})
    user_data["hashed_password"] = hashed_password

    new_user = models.User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user




# Get User by ID

@router.get("/{Id}", status_code= status.HTTP_200_OK , response_model=schemas.user.UserResponse)
def get_user_by_id(Id: int, db: Session = Depends(get_db), current_admin: str = Depends(oauth2.get_current_admin)):
    user_id = db.query(models.User).filter(models.User.id == Id).first()
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user_id



# Update User by ID

@router.put("/{Id}", status_code=status.HTTP_200_OK, response_model=schemas.user.UserResponse)
def update_user_by_id(Id: int, data: schemas.user.UserUpdate, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
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

    return user


# Delete User by ID

@router.delete("/{Id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(Id: int, db: Session = Depends(get_db), current_user: str = Depends(oauth2.get_current_user)):
    query = db.query(models.User).filter(models.User.id == Id)
    user = query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {Id} not found")
    query.delete(synchronize_session=False)
    db.commit()
    return None
    