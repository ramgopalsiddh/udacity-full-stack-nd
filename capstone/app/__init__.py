from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# Configure database
database_path = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://ram@localhost:5432/capstone"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    actors = db.relationship("Actor", backref="movie", lazy=True)

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
            "release_date": self.release_date.strftime("%Y-%m-%d %H:%M:%S"),
            "actors": [actor.format() for actor in self.actors],
        }


class Actor(db.Model):
    __tablename__ = "actors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), nullable=True)

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


# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/movies")
def movies():
    movies_data = Movie.query.all()
    return render_template("movies.html", movies=movies_data)

@app.route("/actors")
def actors():
    actors_data = Actor.query.all()
    return render_template("actors.html", actors=actors_data)

if __name__ == "__main__":
    app.run()

