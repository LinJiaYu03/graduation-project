from pydantic import BaseModel
from typing import Optional


class CampusInfoRequest(BaseModel):
    schoolName: Optional[str] = None
    collegeName: Optional[str] = None
    className: Optional[str] = None
    level: Optional[int] = None
    parentId: Optional[int] = None
    sort: Optional[int] = None
    status: Optional[int] = None
