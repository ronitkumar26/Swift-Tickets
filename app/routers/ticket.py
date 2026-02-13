from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.database.sessions import get_db
from app import models, schemas
from app.core.oauth2 import get_current_user, get_current_admin
from app.models.user import UserRole
from app.models.ticket import TicketStatus

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]
)

# =========================================================
# CREATE TICKET (EMPLOYEE)
# =========================================================

@router.post("/", response_model=schemas.ticket.TicketResponse)
def create_ticket(
    data: schemas.ticket.TicketCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    # Get all tech users
    techs = db.query(models.User).filter(
        models.User.role == UserRole.TECH
    ).all()

    assigned_tech_id = None

    for tech in techs:
        active_count = db.query(models.Ticket).filter(
            models.Ticket.assigned_to_id == tech.id,
            models.Ticket.status.in_([
                TicketStatus.OPEN,
                TicketStatus.IN_PROGRESS
            ])
        ).count()

        if active_count == 0:
            assigned_tech_id = tech.id
            break

    ticket = models.Ticket(
        title=data.title,
        description=data.description,
        priority=data.priority,
        owner_id=current_user.id,
        assigned_to_id=assigned_tech_id
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


# =========================================================
# VIEW MY TICKETS (EMPLOYEE)
# =========================================================

@router.get("/me", response_model=list[schemas.ticket.TicketResponse])
def get_my_tickets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return db.query(models.Ticket).options(
        joinedload(models.Ticket.owner),
        joinedload(models.Ticket.assigned_to)
    ).filter(
        models.Ticket.owner_id == current_user.id
    ).all()

# =========================================================
# VIEW ASSIGNED TICKETS (TECH)
# =========================================================

@router.get("/assigned", response_model=list[schemas.ticket.TicketResponse])
def get_assigned_tickets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role != UserRole.TECH:
        raise HTTPException(status_code=403, detail="Only tech allowed")

    return db.query(models.Ticket).options(
        joinedload(models.Ticket.owner),
        joinedload(models.Ticket.assigned_to)
    ).filter(
        models.Ticket.assigned_to_id == current_user.id
    ).all()


# =========================================================
# EMPLOYEE UPDATE (ONLY OWN TITLE/DESCRIPTION)
# =========================================================

@router.put("/employee/{ticket_id}", response_model=schemas.ticket.TicketResponse)
def employee_update(
    ticket_id: int,
    data: schemas.ticket.TicketEmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(404, "Ticket not found")

    if ticket.owner_id != current_user.id:
        raise HTTPException(403, "Not allowed")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(ticket, key, value)

    db.commit()
    db.refresh(ticket)

    return ticket

# =========================================================
# TECH UPDATE STATUS / RESOLUTION
# =========================================================

@router.put("/tech/{ticket_id}", response_model=schemas.ticket.TicketResponse)
def tech_update(
    ticket_id: int,
    data: schemas.ticket.TicketTechUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role != UserRole.TECH:
        raise HTTPException(403, "Only tech allowed")

    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(404, "Ticket not found")

    if ticket.assigned_to_id != current_user.id:
        raise HTTPException(403, "Not assigned to you")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(ticket, key, value)

    db.commit()
    db.refresh(ticket)

    return ticket

# =========================================================
# ADMIN VIEW ALL
# =========================================================

@router.get("/", response_model=list[schemas.ticket.TicketResponse])
def get_all(
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin),
):
    return db.query(models.Ticket).options(
        joinedload(models.Ticket.owner),
        joinedload(models.Ticket.assigned_to)
    ).all()

# =========================================================
# ADMIN ASSIGN TICKET
# =========================================================


@router.put("/assign/{ticket_id}", response_model=schemas.ticket.TicketResponse)
def assign_ticket(
    ticket_id: int,
    data: schemas.ticket.TicketAssign,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin),
):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(404, "Ticket not found")

    ticket.assigned_to_id = data.assigned_to_id

    db.commit()
    db.refresh(ticket)

    return ticket


# =========================================================
# ADMIN DELETE
# =========================================================

@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_admin: models.User = Depends(get_current_admin),
):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(404, "Ticket not found")

    db.delete(ticket)
    db.commit()

    return None
