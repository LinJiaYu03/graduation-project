from fastapi import APIRouter, Body, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.respones import error_response, page_result, success_response
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
    try:
        activity = activity_services.create_activity(db, request)
        return success_response(data={"activity": activity}, message="创建活动成功")
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="创建活动失败: " + str(e))


@activity_router.put("/update")
def update_activity(request: ActivityUpdateRequest, db: Session = Depends(get_db)):
    try:
        activity = activity_services.update_activity(db, request)
        return success_response(
            data={"activity": activity}, message="编辑活动成功，活动已重新进入审核状态"
        )
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="编辑活动失败: " + str(e))


@activity_router.get("/pending")
def pending_activities(
    bossUserId: int,
    currentPage: int = 1,
    pageSize: int = 10,
    db: Session = Depends(get_db),
):
    try:
        total, current, size, records = activity_services.pending_activities(
            db, bossUserId, currentPage, pageSize
        )
        return success_response(
            data={"page": page_result(total, current, size, records)}, message="查询成功"
        )
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="查询失败: " + str(e))


@activity_router.post("/review")
def review_activity(request: ActivityReviewRequest, db: Session = Depends(get_db)):
    try:
        activity_services.review_activity(db, request)
        return success_response(message="审核成功")
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="审核失败: " + str(e))


@activity_router.post("/registrations/review")
def review_registration(request: RegistrationReviewRequest, db: Session = Depends(get_db)):
    try:
        activity_services.review_registration(db, request)
        return success_response(message="审核成功")
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="审核失败: " + str(e))


@activity_router.post("/search")
def search_activities(request: ActivitySearchRequest, db: Session = Depends(get_db)):
    try:
        total, current, size, records = activity_services.search_activities(db, request)
        return success_response(
            data={"page": page_result(total, current, size, records)}, message="查询成功"
        )
    except Exception as e:
        return error_response(message="查询失败: " + str(e))


@activity_router.get("/hot")
def hot_activities(db: Session = Depends(get_db)):
    try:
        activities = activity_services.hot_activities(db)
        return success_response(data={"activities": activities}, message="查询成功")
    except Exception as e:
        return error_response(message="查询失败: " + str(e))


@activity_router.get("/club/{clubId}")
def activities_by_club(
    clubId: int,
    currentPage: int = 1,
    pageSize: int = 10,
    db: Session = Depends(get_db),
):
    try:
        total, current, size, records = activity_services.activities_by_club(
            db, clubId, currentPage, pageSize
        )
        return success_response(
            data={"page": page_result(total, current, size, records)}, message="查询成功"
        )
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="查询失败: " + str(e))


@activity_router.post("/comment")
def comment_activity(request: ActivityCommentRequest, db: Session = Depends(get_db)):
    try:
        activity_services.comment_activity(db, request)
        return success_response(message="评价成功")
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="评价失败: " + str(e))


@activity_router.post("/checkin")
def checkin(payload: dict = Body(...), db: Session = Depends(get_db)):
    try:
        result = activity_services.checkin(db, payload)
        return success_response(data={"checkin": result}, message="签到成功")
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="签到失败: " + str(e))


@activity_router.get("/user/{userId}")
def user_activities(
    userId: int,
    type: str = "all",
    keyword: str | None = None,
    db: Session = Depends(get_db),
):
    try:
        data = activity_services.user_activities(db, userId, type, keyword)
        return success_response(data=data, message="查询成功")
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="查询失败: " + str(e))


# ---------------------------------------------------------------------------
# 动态路径
# ---------------------------------------------------------------------------

@activity_router.get("/{id}")
def get_activity_detail(
    id: int, managerUserId: int | None = None, db: Session = Depends(get_db)
):
    try:
        data = activity_services.get_activity_detail(db, id)
        return success_response(data=data, message="查询成功")
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="查询失败: " + str(e))


@activity_router.get("/{activityId}/registrations/pending")
def pending_registrations(
    activityId: int, managerUserId: int, db: Session = Depends(get_db)
):
    try:
        items = activity_services.pending_registrations(db, activityId, managerUserId)
        return success_response(data={"items": items}, message="查询成功")
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="查询失败: " + str(e))


@activity_router.get("/{activityId}/registrations/status")
def registration_status(
    activityId: int, managerUserId: int, db: Session = Depends(get_db)
):
    try:
        items = activity_services.registration_status(db, activityId, managerUserId)
        return success_response(data={"items": items}, message="查询成功")
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="查询失败: " + str(e))


@activity_router.get("/{activityId}/registrations/check")
def check_registration(activityId: int, userId: int, db: Session = Depends(get_db)):
    try:
        result = activity_services.check_registration(db, activityId, userId)
        return success_response(data={"registration": result}, message="查询成功")
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="查询失败: " + str(e))


@activity_router.get("/{activityId}/statistics")
def activity_statistics(
    activityId: int, managerUserId: int, db: Session = Depends(get_db)
):
    try:
        statistics = activity_services.activity_statistics(db, activityId, managerUserId)
        return success_response(data={"statistics": statistics}, message="查询成功")
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="查询失败: " + str(e))


@activity_router.get("/{activityId}/checkin-statistics")
def checkin_statistics(
    activityId: int, managerUserId: int, db: Session = Depends(get_db)
):
    try:
        statistics = activity_services.checkin_statistics(db, activityId, managerUserId)
        return success_response(data={"statistics": statistics}, message="查询成功")
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="查询失败: " + str(e))


@activity_router.get("/{activityId}/score-statistics")
def score_statistics(activityId: int, managerUserId: int, db: Session = Depends(get_db)):
    try:
        statistics = activity_services.score_statistics(db, activityId, managerUserId)
        return success_response(data={"statistics": statistics}, message="查询成功")
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="查询失败: " + str(e))


@activity_router.get("/{activityId}/qrcode")
def generate_qrcode(activityId: int, db: Session = Depends(get_db)):
    try:
        qrcode_data = activity_services.generate_qrcode(db, activityId)
        return success_response(data={"qrcode": qrcode_data}, message="生成二维码成功")
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="生成二维码失败: " + str(e))


@activity_router.post("/{activityId}/register")
def register_activity(
    activityId: int, request: ActivityRegisterRequest, db: Session = Depends(get_db)
):
    try:
        registration = activity_services.register_activity(db, activityId, request)
        return success_response(data={"registration": registration}, message="报名成功")
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="报名失败: " + str(e))


@activity_router.put("/{activityId}/publish-status")
def update_publish_status(
    activityId: int, payload: dict = Body(...), db: Session = Depends(get_db)
):
    try:
        message, activity = activity_services.update_publish_status(
            db, activityId, payload
        )
        return success_response(data={"activity": activity}, message=message)
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="操作失败: " + str(e))


@activity_router.delete("/{activityId}")
def delete_activity(activityId: int, managerUserId: int, db: Session = Depends(get_db)):
    try:
        activity_services.delete_activity(db, activityId, managerUserId)
        return success_response(message="删除成功")
    except ValueError as e:
        return error_response(message=str(e))
    except Exception as e:
        return error_response(message="删除失败: " + str(e))


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
