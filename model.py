# -----------------------------------------------------------------------------------------#
#                             IMPORTS
# -----------------------------------------------------------------------------------------#
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

# -----------------------------------------------------------------------------------------#
#                     SET ORM MODEL ClASSES FOR DB
# -----------------------------------------------------------------------------------------#

# Make the engine
engine = create_engine("sqlite+pysqlite:///:memory:", future=True, echo=False)

# Make the DeclarativeMeta
Base = declarative_base()
db = SQLAlchemy()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    password = Column(String(25), nullable=False)
    cities = relationship("City", secondary='user_cities', back_populates='users')


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    users = relationship('User', secondary='user_cities', back_populates='cities')


class UserCities(Base):
    __tablename__ = "user_cities"

    id = Column(Integer, primary_key=True),
    user_Id = Column(Integer, ForeignKey('users.id')),
    city_Id = Column(Integer, ForeignKey('cities.id'))

# -----------------------------------------------------------------------------------------#
#                         Initialize DB
# -----------------------------------------------------------------------------------------#


Base.metadata.create_all(engine)


# -----------------------------------------------------------------------------------------#
#                            DB TESTS
# -----------------------------------------------------------------------------------------#
with Session(bind=engine) as session:

    # add users
    usr1 = User(username="bob", password="pass123")
    session.add(usr1)

    usr2 = User(username="alice", password="password1")
    session.add(usr2)

    session.commit()

    # add cities
    city1 = City(name="Miami")
    session.add(city1)

    city2 = City(name="Orlando")
    session.add(city2)

    session.commit()

    # map users to cities
    city1.users = [usr1, usr2]
    city2.users = [usr2]

    session.commit()


with Session(bind=engine) as session:

    print(session.query(User).where(User.id == 1).one().cities)
    print(session.query(City).where(City.id == 1).one().users)

