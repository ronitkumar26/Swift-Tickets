from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
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
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True , nullable= False)
    hashed_password: Mapped[str] = mapped_column(String, unique= True, nullable= False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), nullable=False, default=UserRole.EMPLOYEE)
    is_active: Mapped[bool] = mapped_column(Boolean, default= True)

    #relationship

    owned_tickets = relationship(
    "Ticket",
    back_populates="owner",
    foreign_keys="Ticket.owner_id",
)

    assigned_tickets = relationship(
    "Ticket",
    back_populates="assigned_to",
    foreign_keys="Ticket.assigned_to_id",
)


