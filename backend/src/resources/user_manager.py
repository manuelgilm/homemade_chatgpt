from src.db.models.user import User
from src.auth.schemas import UserCreateModel
from src.auth.utils import generate_passwd_hash
from sqlmodel import Session
from sqlmodel import select
from typing import Optional


class UserManager:

    def create_user(self, session: Session, user_data: UserCreateModel) -> User:
        user_data_dict = user_data.model_dump()
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

    def get_user(self):
        pass

    def update_user(self):
        pass

    def delete_user(self):
        pass

    def list_users(self):
        pass
