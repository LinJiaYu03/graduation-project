from sqlalchemy.orm import Session

from app.models.campus_info import CampusInfo
from app.schemas.campus import CampusInfoRequest


def _has_text(v) -> bool:
    return v is not None and str(v).strip() != ""


def build_campus_tree(db: Session) -> list[dict]:
    infos = (
        db.query(CampusInfo)
        .filter(CampusInfo.status == 1)
        .order_by(CampusInfo.level.asc(), CampusInfo.sort.asc(), CampusInfo.id.asc())
        .all()
    )

    school_map: dict[int, dict] = {}
    college_map: dict[int, dict] = {}

    for info in infos:
        if info.level is None:
            continue
        if info.level == 1:
            if info.id not in school_map:
                school_map[info.id] = {"id": info.id, "name": info.school_name, "colleges": []}
        elif info.level == 2:
            school_node = school_map.get(info.parent_id)
            if school_node is not None and info.id not in college_map:
                college = {"id": info.id, "name": info.college_name, "classes": []}
                college_map[info.id] = college
                school_node["colleges"].append(college)
        elif info.level == 3:
            college_node = college_map.get(info.parent_id)
            if college_node is not None and _has_text(info.class_name):
                college_node["classes"].append({"id": info.id, "name": info.class_name})

    return list(school_map.values())


def create_campus(db: Session, request: CampusInfoRequest) -> list[int]:
    """对齐 CampusInfoController.createCampusInfo：逐级创建学校/学院/班级"""
    if not _has_text(request.schoolName):
        raise ValueError("学校名称不能为空")

    created_ids: list[int] = []

    # 1. 学校（level=1）
    school = (
        db.query(CampusInfo)
        .filter(CampusInfo.school_name == request.schoolName, CampusInfo.level == 1)
        .first()
    )
    if school is None:
        school = CampusInfo(
            school_name=request.schoolName,
            level=1,
            parent_id=None,
            sort=request.sort if request.sort is not None else 0,
            status=request.status if request.status is not None else 1,
        )
        db.add(school)
        db.commit()
        db.refresh(school)
        created_ids.append(school.id)
    school_id = school.id

    # 2. 学院（level=2）
    college_id = None
    if _has_text(request.collegeName):
        college = (
            db.query(CampusInfo)
            .filter(
                CampusInfo.school_name == request.schoolName,
                CampusInfo.college_name == request.collegeName,
                CampusInfo.level == 2,
                CampusInfo.parent_id == school_id,
            )
            .first()
        )
        if college is None:
            college = CampusInfo(
                school_name=request.schoolName,
                college_name=request.collegeName,
                level=2,
                parent_id=school_id,
                sort=request.sort if request.sort is not None else 0,
                status=request.status if request.status is not None else 1,
            )
            db.add(college)
            db.commit()
            db.refresh(college)
            created_ids.append(college.id)
        college_id = college.id

    # 3. 班级（level=3）
    if _has_text(request.className):
        if college_id is None:
            raise ValueError("创建班级需要提供学院名称")
        clazz = (
            db.query(CampusInfo)
            .filter(
                CampusInfo.school_name == request.schoolName,
                CampusInfo.college_name == request.collegeName,
                CampusInfo.class_name == request.className,
                CampusInfo.level == 3,
                CampusInfo.parent_id == college_id,
            )
            .first()
        )
        if clazz is None:
            clazz = CampusInfo(
                school_name=request.schoolName,
                college_name=request.collegeName,
                class_name=request.className,
                level=3,
                parent_id=college_id,
                sort=request.sort if request.sort is not None else 0,
                status=request.status if request.status is not None else 1,
            )
            db.add(clazz)
            db.commit()
            db.refresh(clazz)
            created_ids.append(clazz.id)

    return created_ids
