from src.api.db.models.user import User
from src.api.auth.schemas import UserCreateModel
from src.api.auth.utils import generate_passwd_hash
from sqlmodel import Session
from sqlmodel import select
from typing import Optional


class UserManager:

    def __init__(self):
        print("UserManager initialized")

    def create_user(
        self, session: Session, user_data: UserCreateModel, role: Optional[str] = "user"
    ) -> User:
        user_data_dict = user_data.model_dump()
        user_data_dict["role"] = role
        new_user = User(**user_data_dict)
        new_user.hashed_password = generate_passwd_hash(
            password=user_data_dict["password"]
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user

    def user_exists(self, email: str, session: Session) -> bool:
        user = self.get_user_by_email(email=email, session=session)
        if user:
            return True
        return False

    def get_user_by_email(self, email: str, session: Session) -> Optional[User]:
        statement = select(User).where(User.email == email)
        result = session.exec(statement).first()
        return result

    def list_users(self, session: Session):
        statement = select(User)
        result = session.exec(statement).all()
        return result
