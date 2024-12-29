from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text(255))

    tools = relationship('Tool', back_populates='user')

    def __str__(self):
        return self.name


class Types(Base):
    __tablename__ = 'types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45), nullable=False, unique=True)

    tools = relationship('Tool', back_populates='types')

    def __str__(self):
        return self.name


class Tool(Base):
    __tablename__ = 'tool'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    types_id = Column(Integer, ForeignKey('types.id'))
    name_tool = Column(String(255), nullable=False)
    tool_photo = Column(String(255))
    added_year = Column(Integer, nullable=False)

    user = relationship('User', back_populates='tools')
    types = relationship('Types', back_populates='tools')

