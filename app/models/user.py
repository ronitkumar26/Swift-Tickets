from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base
from enum import Enum
from sqlalchemy import Enum as SQLEnum
from app.database.mixins import TimestampMixin

class UserRole(str, Enum):
    EMPLOYEE = "employee"
    TECH = "tech"
    ADMIN = "admin"

class User(Base, TimestampMixin):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True , nullable= False)
    hashed_password: Mapped[str] = mapped_column(String, unique= True, nullable= False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), nullable=False, default=UserRole.EMPLOYEE)
    is_active: Mapped[Boolean] = mapped_column(Boolean, default= True)

