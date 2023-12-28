# models.py

from flask_sqlalchemy import SQLAlchemy
import os

# database_path = os.getenv("DATABASE_URL")
db = SQLAlchemy()

# Association Table
actor_movie_association = db.Table(
    "actor_movie_association",
    db.Column("actor_id", db.Integer, db.ForeignKey("actors.id")),
    db.Column("movie_id", db.Integer, db.ForeignKey("movies.id")),
)


class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://ram@localhost:5432/capstone"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


"""
Movie Model
"""


class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)

    # Define the many-to-many relationship
    actors = db.relationship(
        "Actor", secondary=actor_movie_association, back_populates="movies"
    )

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

    def format(self, skip_actors=False):
        formatted_movie = {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
        }

        if not skip_actors:
            formatted_movie["actors"] = [
                actor.format(skip_movies=True) for actor in self.actors
            ]

        return formatted_movie


"""
Actor's Model
"""


class Actor(db.Model):
    __tablename__ = "actors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)

    # Define the many-to-many relationship
    movies = db.relationship(
        "Movie", secondary=actor_movie_association, back_populates="actors"
    )

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self, skip_movies=False):
        formatted_actor = {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
        }

        if not skip_movies:
            formatted_actor["movies"] = [
                movie.format(skip_actors=True) for movie in self.movies
            ]

        return formatted_actor
