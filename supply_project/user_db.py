
from sqlalchemy.exc import SQLAlchemyError
from models import User
from config import Session


def get_user():
    try:

        with Session() as session:
            user = session.query(User).all()

            return user

    except SQLAlchemyError as e:
        print(e)


def save_user(user):
    with Session() as session:
        session.add(user)
        session.commit()


def delete_user(user):
    with Session() as session:
        session.delete(user)
        session.commit()


def update_user(user):
    with Session() as session:
        session.merge(user)
        session.commit()