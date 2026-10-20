from fastapi import APIRouter, Body, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.activity import (
    ActivityCommentRequest,
    ActivityCreateRequest,
    ActivityRegisterRequest,
    ActivityReviewRequest,
    ActivitySearchRequest,
    ActivityUpdateRequest,
    RegistrationReviewRequest,
)
from app.services import activity_services

activity_router = APIRouter()


@activity_router.post("/create")
def create_activity(request: ActivityCreateRequest, db: Session = Depends(get_db)):
    return activity_services.create_activity(db, request)


@activity_router.put("/update")
def update_activity(request: ActivityUpdateRequest, db: Session = Depends(get_db)):
    return activity_services.update_activity(db, request)


@activity_router.get("/pending")
def pending_activities(
    bossUserId: int,
    currentPage: int = 1,
    pageSize: int = 10,
    db: Session = Depends(get_db),
):
    return activity_services.pending_activities(db, bossUserId, currentPage, pageSize)


@activity_router.post("/review")
def review_activity(request: ActivityReviewRequest, db: Session = Depends(get_db)):
    return activity_services.review_activity(db, request)


@activity_router.post("/registrations/review")
def review_registration(request: RegistrationReviewRequest, db: Session = Depends(get_db)):
    return activity_services.review_registration(db, request)


@activity_router.post("/search")
def search_activities(request: ActivitySearchRequest, db: Session = Depends(get_db)):
    return activity_services.search_activities(db, request)


@activity_router.get("/hot")
def hot_activities(db: Session = Depends(get_db)):
    return activity_services.hot_activities(db)


@activity_router.get("/club/{clubId}")
def activities_by_club(
    clubId: int,
    currentPage: int = 1,
    pageSize: int = 10,
    db: Session = Depends(get_db),
):
    return activity_services.activities_by_club(db, clubId, currentPage, pageSize)


@activity_router.post("/comment")
def comment_activity(request: ActivityCommentRequest, db: Session = Depends(get_db)):
    return activity_services.comment_activity(db, request)


@activity_router.post("/checkin")
def checkin(payload: dict = Body(...), db: Session = Depends(get_db)):
    return activity_services.checkin(db, payload)


@activity_router.get("/user/{userId}")
def user_activities(
    userId: int,
    type: str = "all",
    keyword: str | None = None,
    db: Session = Depends(get_db),
):
    return activity_services.user_activities(db, userId, type, keyword)


# ---------------------------------------------------------------------------
# 动态路径
# ---------------------------------------------------------------------------

@activity_router.get("/{id}")
def get_activity_detail(
    id: int, managerUserId: int | None = None, db: Session = Depends(get_db)
):
    return activity_services.get_activity_detail(db, id)


@activity_router.get("/{activityId}/registrations/pending")
def pending_registrations(
    activityId: int, managerUserId: int, db: Session = Depends(get_db)
):
    return activity_services.pending_registrations(db, activityId, managerUserId)


@activity_router.get("/{activityId}/registrations/status")
def registration_status(
    activityId: int, managerUserId: int, db: Session = Depends(get_db)
):
    return activity_services.registration_status(db, activityId, managerUserId)


@activity_router.get("/{activityId}/registrations/check")
def check_registration(activityId: int, userId: int, db: Session = Depends(get_db)):
    return activity_services.check_registration(db, activityId, userId)


@activity_router.get("/{activityId}/statistics")
def activity_statistics(
    activityId: int, managerUserId: int, db: Session = Depends(get_db)
):
    return activity_services.activity_statistics(db, activityId, managerUserId)


@activity_router.get("/{activityId}/checkin-statistics")
def checkin_statistics(
    activityId: int, managerUserId: int, db: Session = Depends(get_db)
):
    return activity_services.checkin_statistics(db, activityId, managerUserId)


@activity_router.get("/{activityId}/score-statistics")
def score_statistics(activityId: int, managerUserId: int, db: Session = Depends(get_db)):
    return activity_services.score_statistics(db, activityId, managerUserId)


@activity_router.get("/{activityId}/qrcode")
def generate_qrcode(activityId: int, db: Session = Depends(get_db)):
    return activity_services.generate_qrcode(db, activityId)


@activity_router.post("/{activityId}/register")
def register_activity(
    activityId: int, request: ActivityRegisterRequest, db: Session = Depends(get_db)
):
    return activity_services.register_activity(db, activityId, request)


@activity_router.put("/{activityId}/publish-status")
def update_publish_status(
    activityId: int, payload: dict = Body(...), db: Session = Depends(get_db)
):
    return activity_services.update_publish_status(db, activityId, payload)


@activity_router.delete("/{activityId}")
def delete_activity(activityId: int, managerUserId: int, db: Session = Depends(get_db)):
    return activity_services.delete_activity(db, activityId, managerUserId)


# ---------------------------------------------------------------------------
# Excel 导出（二进制响应）
# ---------------------------------------------------------------------------

def _excel_response(content: bytes, filename: str) -> Response:
    return Response(
        content=content,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": activity_services.export_disposition(filename)},
    )


def _export_error(e: Exception) -> Response:
    if isinstance(e, activity_services.ExportError):
        return Response(
            content=e.message,
            status_code=e.status_code,
            media_type="text/plain; charset=utf-8",
        )
    return Response(
        content="导出失败: " + str(e),
        status_code=500,
        media_type="text/plain; charset=utf-8",
    )


@activity_router.get("/{activityId}/export/registration")
def export_registration(activityId: int, managerUserId: int, db: Session = Depends(get_db)):
    try:
        content, filename = activity_services.export_registration(
            db, activityId, managerUserId
        )
    except Exception as e:
        return _export_error(e)
    return _excel_response(content, filename)


@activity_router.get("/{activityId}/export/checkin")
def export_checkin(activityId: int, managerUserId: int, db: Session = Depends(get_db)):
    try:
        content, filename = activity_services.export_checkin(db, activityId, managerUserId)
    except Exception as e:
        return _export_error(e)
    return _excel_response(content, filename)


@activity_router.get("/{activityId}/export/score")
def export_score(activityId: int, managerUserId: int, db: Session = Depends(get_db)):
    try:
        content, filename = activity_services.export_score(db, activityId, managerUserId)
    except Exception as e:
        return _export_error(e)
    return _excel_response(content, filename)
