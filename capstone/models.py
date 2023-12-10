import os
from sqlalchemy import ForeignKey, Column, String, Integer, DateTime, create_engine
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate

# Database setup

# database_name = "capstone"
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)
# database_path = "postgres:///{}".format(database_name)
database_path = os.getenv("DATABASE_URL")
db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://ram@localhost:5432/capstone"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)


## Movie auth setup
"""
Movie
"""


class Movie(db.Model):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(DateTime)
    actors = relationship("Actor", backref="movie", lazy=True)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "actors": list(map(lambda actor: actor.format(), self.actors)),
        }


# Actor auth setup
"""
Actor
"""


class Actor(db.Model):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=True)

    def __init__(self, name, age, gender, movie_id):
        self.name = name
        self.age = age
        self.gender = gender
        self.movie_id = movie_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "movie_id": self.movie_id,
        }
