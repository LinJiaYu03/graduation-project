from fastapi import APIRouter, Body, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_permission
from app.core.rbac import Perm
from app.db.database import get_db
from app.models.user import User
from app.schemas.activity import (
    ActivityCommentRequest,
    ActivityCreateRequest,
    ActivityReviewRequest,
    ActivitySearchRequest,
    ActivityUpdateRequest,
    RegistrationReviewRequest,
)
from app.services import activity_services

activity_router = APIRouter()


@activity_router.post("/create")
def create_activity(
    request: ActivityCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return activity_services.create_activity(db, request, current_user)


@activity_router.put("/update")
def update_activity(
    request: ActivityUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return activity_services.update_activity(db, request, current_user)


@activity_router.get("/pending")
def pending_activities(
    currentPage: int = 1,
    pageSize: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Perm.ACTIVITY_REVIEW)),
):
    return activity_services.pending_activities(
        db, current_user, currentPage, pageSize
    )


@activity_router.post("/review")
def review_activity(
    request: ActivityReviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Perm.ACTIVITY_REVIEW)),
):
    return activity_services.review_activity(db, request, current_user)


@activity_router.post("/registrations/review")
def review_registration(
    request: RegistrationReviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return activity_services.review_registration(db, request, current_user)


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
def comment_activity(
    request: ActivityCommentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Perm.ACTIVITY_COMMENT)),
):
    return activity_services.comment_activity(db, request, current_user)


@activity_router.post("/checkin")
def checkin(
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Perm.ACTIVITY_CHECKIN)),
):
    return activity_services.checkin(db, payload, current_user)


@activity_router.get("/user/{userId}")
def user_activities(
    userId: int,
    type: str = "all",
    keyword: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return activity_services.user_activities(
        db, userId, type, keyword, current_user
    )


# ---------------------------------------------------------------------------
# 动态路径
# ---------------------------------------------------------------------------

@activity_router.get("/{id}")
def get_activity_detail(id: int, db: Session = Depends(get_db)):
    return activity_services.get_activity_detail(db, id)


@activity_router.get("/{activityId}/registrations/pending")
def pending_registrations(
    activityId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return activity_services.pending_registrations(db, activityId, current_user)


@activity_router.get("/{activityId}/registrations/status")
def registration_status(
    activityId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return activity_services.registration_status(db, activityId, current_user)


@activity_router.get("/{activityId}/registrations/check")
def check_registration(
    activityId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return activity_services.check_registration(db, activityId, current_user.id)


@activity_router.get("/{activityId}/statistics")
def activity_statistics(
    activityId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return activity_services.activity_statistics(db, activityId, current_user)


@activity_router.get("/{activityId}/checkin-statistics")
def checkin_statistics(
    activityId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return activity_services.checkin_statistics(db, activityId, current_user)


@activity_router.get("/{activityId}/score-statistics")
def score_statistics(
    activityId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return activity_services.score_statistics(db, activityId, current_user)


@activity_router.get("/{activityId}/qrcode")
def generate_qrcode(
    activityId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return activity_services.generate_qrcode(db, activityId, current_user)


@activity_router.post("/{activityId}/register")
def register_activity(
    activityId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission(Perm.ACTIVITY_REGISTER)),
):
    return activity_services.register_activity(db, activityId, current_user)


@activity_router.put("/{activityId}/publish-status")
def update_publish_status(
    activityId: int,
    payload: dict = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return activity_services.update_publish_status(
        db, activityId, payload, current_user
    )


@activity_router.delete("/{activityId}")
def delete_activity(
    activityId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return activity_services.delete_activity(db, activityId, current_user)


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
def export_registration(
    activityId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        content, filename = activity_services.export_registration(
            db, activityId, current_user
        )
    except Exception as e:
        return _export_error(e)
    return _excel_response(content, filename)


@activity_router.get("/{activityId}/export/checkin")
def export_checkin(
    activityId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        content, filename = activity_services.export_checkin(
            db, activityId, current_user
        )
    except Exception as e:
        return _export_error(e)
    return _excel_response(content, filename)


@activity_router.get("/{activityId}/export/score")
def export_score(
    activityId: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        content, filename = activity_services.export_score(
            db, activityId, current_user
        )
    except Exception as e:
        return _export_error(e)
    return _excel_response(content, filename)
