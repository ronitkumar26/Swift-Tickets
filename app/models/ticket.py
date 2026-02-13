from sqlalchemy import String, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.base import Base
from enum import Enum


class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[TicketStatus] = mapped_column(
        SQLEnum(TicketStatus),
        default=TicketStatus.OPEN,
        nullable=False
    )

    priority: Mapped[TicketPriority] = mapped_column(
        SQLEnum(TicketPriority),
        default=TicketPriority.MEDIUM,
        nullable=False
    )

    resolution_note: Mapped[str | None] = mapped_column(Text, nullable=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    assigned_to_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    #Relationships
    owner = relationship(
        "User",
        back_populates="owned_tickets",
        foreign_keys=[owner_id]
    )

    assigned_to = relationship(
        "User",
        back_populates="assigned_tickets",
        foreign_keys=[assigned_to_id]
    )
