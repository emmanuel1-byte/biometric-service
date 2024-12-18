from sqlmodel import Session, select
from .model import User
from .schema import Signup_Schema


def create_user(data: Signup_Schema, session: Session):
    try:
        new_user = User(**data.model_dump())

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return new_user
    except Exception:
        session.rollback()
        raise


def find_user_by_email(email: str, session: Session):
    try:
        user_query = select(User).where(User.email == email)
        result = session.exec(user_query)

        user = result.one_or_none()
        if user is None:
            return None

        return user
    except Exception:
        raise


def find_user_by_id(user_id: str, session: Session):
    try:
        user_query = select(User).where(User.id == user_id)
        result = session.exec(user_query)

        user = result.one_or_none()
        if user is None:
            return None

        return user
    except Exception:
        raise
