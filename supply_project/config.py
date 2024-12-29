# pip install SQLAlchemy
# pip install mysql-connector-python

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Baza MySQL
# engine = create_engine('mysql+mysqlconnector://root:Qweasd123.@localhost:3306/python_projekt')
# Baza SQLLite
DATABASE_URL = 'sqlite:///supply.db'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
