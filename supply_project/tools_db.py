
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from models import Tool, User
from config import Session


def get_tools():
    try:

        with Session() as session:
            tools = session.query(Tool).options(joinedload(Tool.user), joinedload(Tool.types)).all()

            return tools

    except SQLAlchemyError as e:
        print(e)


def save_tool(tool):
    with Session() as session:
        session.add(tool)
        session.commit()


def delete_tool(tool):
    with Session() as session:
        session.delete(tool)
        session.commit()


def update_tool(tool):
    with Session() as session:
        session.merge(tool)
        session.commit()
