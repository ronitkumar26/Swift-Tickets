from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.ticket import TicketStatus, TicketPriority
from app.schemas.user import UserResponse


class TicketCreate(BaseModel):
    title: str
    description: str
    priority: TicketPriority


class TicketEmployeeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class TicketTechUpdate(BaseModel):
    status: Optional[TicketStatus] = None
    resolution_note: Optional[str] = None


class TicketAssign(BaseModel):
    assigned_to_id: int


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    resolution_note: Optional[str]
    owner: UserResponse
    assigned_to: Optional[UserResponse]

    class Config:
        from_attributes = True
