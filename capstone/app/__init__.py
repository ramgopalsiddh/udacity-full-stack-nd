
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, make_response
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Movie, Actor
from flask_migrate import Migrate
from auth.auth import requires_auth, AuthError
import os
import secrets

app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_hex(16)

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
@app.route('/')
@app.route("/login")
def login():
    return render_template("login.html")

# logout 
@app.route('/logout')
def logout():
    # Clear the session and any other user-related data
    session.clear()
    # Redirect to the Auth0 logout URL
    return redirect('https://ramgopalsiddh.us.auth0.com/logout?client_id=nGfqDFBy34G83Nffy4CyajPMMb8hX31Y&returnTo=' + url_for('login', _external=True))


@app.route("/index")
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

@app.route("/edit_movie_form/<int:movie_id>")
def edit_movie_form(movie_id):
    movie = Movie.query.get(movie_id)
    actors = Actor.query.all()
    selected_actors = [actor.id for actor in movie.actors]
    return render_template("edit_movie_form.html", movie=movie, actors=actors, selected_actors=selected_actors)

@app.route("/edit_movie/<int:movie_id>", methods=["POST"])
def edit_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if movie:
        title = request.form.get("title")
        release_date = request.form.get("release_date")
        actors_ids = request.form.getlist("actors")

        movie.title = title
        movie.release_date = release_date
        movie.actors = Actor.query.filter(Actor.id.in_(actors_ids)).all()

        movie.update()

    return redirect(url_for("movies"))

@app.route("/edit_actor_form/<int:actor_id>")
def edit_actor_form(actor_id):
    actor = Actor.query.get(actor_id)
    return render_template("edit_actor_form.html", actor=actor)

@app.route("/edit_actor/<int:actor_id>", methods=["POST"])
def edit_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if actor:
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        movie_id = request.form.get("movie_id")

        actor.name = name
        actor.age = age
        actor.gender = gender
        actor.movie_id = movie_id

        actor.update()

    return redirect(url_for("actors"))

@app.route('/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if movie:
        movie.delete()
    return redirect(url_for('movies'))  # Redirect to the movies page or home page

@app.route('/delete_actor/<int:actor_id>', methods=['POST'])
def delete_actor(actor_id):
    actor = Actor.query.get(actor_id)
    if actor:
        actor.delete()
    return redirect(url_for('actors'))  # Redirect to the actors page or home page

if __name__ == "__main__":
    app.run()

