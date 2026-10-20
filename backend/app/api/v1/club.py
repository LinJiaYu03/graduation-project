from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.club import (
    ClubRequest,
    ClubSearchRequest,
    JoinClubRequest,
    JoinedClubSearchRequest,
)
from app.services import club_services

club_router = APIRouter()


@club_router.post("/create")
def create_club(request: ClubRequest, db: Session = Depends(get_db)):
    return club_services.create_club(db, request)


@club_router.post("/search")
def search_clubs(request: ClubSearchRequest, db: Session = Depends(get_db)):
    return club_services.search_clubs(db, request)


@club_router.post("/join")
def join_club(request: JoinClubRequest, db: Session = Depends(get_db)):
    return club_services.join_club(db, request.clubId, request.userId)


@club_router.post("/joined")
def get_joined_clubs(request: JoinedClubSearchRequest, db: Session = Depends(get_db)):
    return club_services.joined_clubs(db, request)


@club_router.get("/managed")
def get_managed_clubs(userId: int, db: Session = Depends(get_db)):
    return club_services.managed_clubs(db, userId)


@club_router.get("/latest")
def get_latest_clubs(limit: int = 4, db: Session = Depends(get_db)):
    return club_services.latest_clubs(db, limit)


@club_router.get("/{clubId}/members")
def get_club_members(clubId: int, db: Session = Depends(get_db)):
    return club_services.club_members(db, clubId)


@club_router.post("/{clubId}/members/{userId}/manager")
def set_club_member_manager(
    clubId: int, userId: int, isManager: bool = True, db: Session = Depends(get_db)
):
    return club_services.set_manager(db, clubId, userId, isManager)


@club_router.get("/{id}")
def get_club_by_id(id: int, db: Session = Depends(get_db)):
    return club_services.get_club(db, id)
