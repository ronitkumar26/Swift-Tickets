from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.database.sessions import get_db
from app import models, schemas
from app.core.security import hash_password
from app.core.oauth2 import get_current_user, get_current_admin


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# =========================================================
# SELF ROUTES (Logged-in User)
# =========================================================

# Get current logged-in user
@router.get("/me", response_model=schemas.user.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user

#Update current logged-in user
@router.put("/me", response_model=schemas.user.UserResponse)
def update_me(
    data: schemas.user.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    update_data = data.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))

    update_data.pop("role", None)
    update_data.pop("hashed_password", None)

    for key, value in update_data.items():
        setattr(current_user, key, value)

    db.commit()
    db.refresh(current_user)
    return current_user


# Delete own account
@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_me(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db.delete(current_user)
    db.commit()
    return None


# =========================================================
# ADMIN ROUTES
# =========================================================

# Get all users (Admin only)
@router.get("/", response_model=list[schemas.user.UserResponse])
def get_users(db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin)):
    users = db.query(models.User).all()
    return users


# Get user by ID (Admin only)
@router.get("/{id}", response_model=schemas.user.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )

    return user


# Update user by ID (Admin only)
@router.put("/{id}", response_model=schemas.user.UserResponse)
def update_user_by_id(id: int, data: schemas.user.UserUpdate, db: Session = Depends(get_db), current_admin: models.User = 
                      Depends(get_current_admin)):
    
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


# Delete user by ID (Admin only)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} not found",
        )

    db.delete(user)
    db.commit()

    return None


# =========================================================
# PUBLIC ROUTE (Registration)
# =========================================================

# Create user (Registration)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.user.UserResponse)
def create_user(data: schemas.user.UserCreate, db: Session = Depends(get_db)):
    hashed_pw = hash_password(data.password)

    new_user = models.User(
        username=data.username,
        email=data.email,
        hashed_password=hashed_pw,
        role=data.role.EMPLOYEE
    )   

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# =========================================================
# ADMIN ROUTE (Registration)
# =========================================================


@router.post("/admin-create", response_model=schemas.user.UserResponse)
def admin_create_user(
    data: schemas.user.UserCreate,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin)
):

    hashed_pw = hash_password(data.password)

    new_user = models.User(
        username=data.username,
        email=data.email,
        hashed_password=hashed_pw,
        role=data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
