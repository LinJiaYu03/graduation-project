from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.campus import CampusInfoRequest
from app.services import campus_services

campus_router = APIRouter()


@campus_router.get("/tree")
def get_campus_tree(db: Session = Depends(get_db)):
    return campus_services.build_campus_tree(db)


@campus_router.post("/create")
def create_campus(request: CampusInfoRequest, db: Session = Depends(get_db)):
    return campus_services.create_campus(db, request)
