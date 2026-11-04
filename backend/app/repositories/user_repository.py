from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """用户表的数据访问。事务边界由 service 控制，本类不提交。"""

    def __init__(self, db: Session) -> None:
        super().__init__(db, User)

    def get_by_username(self, username: str) -> Optional[User]:
        return self.get_by(username=username)

    def get_by_student_no(self, student_no: str) -> Optional[User]:
        return self.get_by(student_no=student_no)

    def get_by_ids(self, user_ids: list[int]) -> list[User]:
        if not user_ids:
            return []
        return self.db.query(User).filter(User.id.in_(user_ids)).all()

    def username_exists(self, username: str) -> bool:
        return self.exists(username=username)

    def student_no_exists(
        self, student_no: str, exclude_user_id: Optional[int] = None
    ) -> bool:
        query = self.db.query(User).filter(User.student_no == student_no)
        if exclude_user_id is not None:
            query = query.filter(User.id != exclude_user_id)
        return query.first() is not None

    def paginate_users(self, page: int, page_size: int) -> tuple[int, list[User]]:
        return self.paginate(page, page_size)

    def search(
        self, keyword: Optional[str], page: int, page_size: int
    ) -> tuple[int, list[User]]:
        query = self.db.query(User)
        if keyword:
            like = f"%{keyword}%"
            query = query.filter(
                or_(
                    User.username.like(like),
                    User.real_name.like(like),
                    User.student_no.like(like),
                )
            )
        return self.paginate_query(query, page, page_size)

    def create_user(
        self, username: str, password: str, avatar_url: Optional[str] = None
    ) -> User:
        return self.create(
            username=username, password=password, avatar_url=avatar_url
        )

    def delete_by_ids(self, user_ids: list[int]) -> int:
        if not user_ids:
            return 0
        return (
            self.db.query(User)
            .filter(User.id.in_(user_ids))
            .delete(synchronize_session=False)
        )
