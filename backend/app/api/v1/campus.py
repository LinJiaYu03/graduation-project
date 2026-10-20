from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.respones import success_response, error_response
from app.schemas.campus import CampusInfoRequest
from app.services import campus_services

campus_router = APIRouter()


@campus_router.get("/tree")
def get_campus_tree(db: Session = Depends(get_db)):
    return success_response(
        data={"items": campus_services.build_campus_tree(db)}, message="查询成功"
    )


@campus_router.post("/create")
def create_campus(request: CampusInfoRequest, db: Session = Depends(get_db)):
    try:
        created_ids = campus_services.create_campus(db, request)
        return success_response(
            data={"createdIds": created_ids, "count": len(created_ids)}, message="创建成功"
        )
    except ValueError as e:
        return error_response(message=str(e))
