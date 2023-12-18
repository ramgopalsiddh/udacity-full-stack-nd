from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor
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

# Route for displaying actors
@app.route("/actors")
def actors():
    actors_data = Actor.query.all()
    return render_template("actors.html", actors=actors_data)



@app.route('/create_movie_form')
def create_movie_form():
    actors_data = Actor.query.all()
    return render_template('create_movie_form.html', actors=actors_data)

# Route for handling the submission of the "Create Movie" form
@app.route('/create_movie', methods=['POST'])
def create_movie():
    title = request.form.get('title')
    release_date = request.form.get('release_date')
    actor_ids = request.form.getlist('actors')

    new_movie = Movie(title=title, release_date=release_date)
    for actor_id in actor_ids:
        actor = Actor.query.get(actor_id)
        if actor:
            new_movie.actors.append(actor)

    new_movie.insert()

    return redirect(url_for('index'))  # Redirect to the homepage or wherever you want

# Route for displaying the "Create Actor" form
@app.route('/create_actor_form')
def create_actor_form():
    return render_template('create_actor_form.html')

# Route for handling the submission of the "Create Actor" form
@app.route('/create_actor', methods=['POST'])
def create_actor():
    name = request.form.get('name')
    age = request.form.get('age')
    gender = request.form.get('gender')
    movie_id = request.form.get('movie_id')

    new_actor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)
    new_actor.insert()

    return redirect(url_for('index'))  # Redirect to the homepage or wherever you want

if __name__ == "__main__":
    app.run()

