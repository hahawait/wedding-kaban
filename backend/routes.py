from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db
from email_service import send_invitation

router = APIRouter(prefix="/api")


@router.post("/register", response_model=schemas.GuestOut, status_code=201)
def register_guest(guest: schemas.GuestCreate, db: Session = Depends(get_db)):
    if db.query(models.Guest).filter(models.Guest.email == guest.email).first():
        raise HTTPException(status_code=400, detail="Этот email уже зарегистрирован")

    db_guest = models.Guest(name=guest.name, email=guest.email, wish=guest.wish)
    db.add(db_guest)
    db.commit()
    db.refresh(db_guest)

    try:
        send_invitation(db_guest.name, db_guest.email)
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")

    return db_guest


@router.get("/guests", response_model=List[schemas.GuestOut])
def get_guests(db: Session = Depends(get_db)):
    return db.query(models.Guest).order_by(models.Guest.registered_at.desc()).all()


@router.get("/health")
def health():
    return {"status": "ok"}
