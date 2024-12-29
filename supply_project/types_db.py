
from sqlalchemy.exc import SQLAlchemyError
from models import Types
from config import Session


def get_types():
    try:

        with Session() as session:
            types = session.query(Types).all()

            return types

    except SQLAlchemyError as e:
        print(e)

def save_type(type):
    with Session() as session:
        session.add(type)
        session.commit()


def delete_type(type):
    with Session() as session:
        session.delete(type)
        session.commit()


def update_type(type):
    with Session() as session:
        session.merge(type)
        session.commit()