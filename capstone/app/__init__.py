from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Config, Movie, Actor
from flask_migrate import Migrate
from auth.auth import requires_auth
import secrets

migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = secrets.token_hex(16)

    # Configure database
    app.config.from_object(Config)

    # Initialize SQLAlchemy with the app
    db.init_app(app)
    migrate.init_app(app, db)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

    # Routes
    @app.route("/")
    @app.route("/login")
    def login():
        return render_template("login.html")

    # logout
    @app.route("/logout")
    def logout():
        # Clear the session and any other user-related data
        session.clear()
        # Redirect to the Auth0 logout URL
        return redirect(
            "https://ramgopalsiddh.us.auth0.com/logout?client_id=nGfqDFBy34G83Nffy4CyajPMMb8hX31Y&returnTo="
            + url_for("login", _external=True)
        )

    @app.route("/index")
    def index():
        return render_template("index.html")

    @app.route("/movies", methods=["GET"])
    @requires_auth("view:movies")
    def movies(payload):
        movies = Movie.query.all()
        movies = list(map(lambda movie: movie.format(), movies))
        return jsonify({"success": True, "movies": movies})
        # movies_data = Movie.query.all()
        # return render_template("movies.html", movies=movies_data)

    @app.route("/view-movies", methods=["GET"])
    def view_movies():
        return render_template("movies.html")

    # Route for displaying actors
    @app.route("/actors", methods=["GET"])
    def actors():
        actors_data = Actor.query.all()
        return render_template("actors.html", actors=actors_data)

    @app.route("/create_movie_form")
    def create_movie_form():
        actors_data = Actor.query.all()
        return render_template("create_movie_form.html", actors=actors_data)

    # Route for handling the submission of the "Create Movie" form
    @app.route("/create_movie", methods=["POST"])
    def create_movie():
        title = request.form.get("title")
        release_date = request.form.get("release_date")
        actor_ids = request.form.getlist("actors")

        new_movie = Movie(title=title, release_date=release_date)
        for actor_id in actor_ids:
            actor = Actor.query.get(actor_id)
            if actor:
                new_movie.actors.append(actor)

        new_movie.insert()

        return redirect(
            url_for("index")
        )  # Redirect to the homepage or wherever you want

    # Route for displaying the "Create Actor" form
    @app.route("/create_actor_form")
    def create_actor_form():
        return render_template("create_actor_form.html")

    # Route for handling the submission of the "Create Actor" form
    @app.route("/create_actor", methods=["POST"])
    def create_actor():
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        movie_id = request.form.get("movie_id")

        new_actor = Actor(name=name, age=age, gender=gender, movie_id=movie_id)
        new_actor.insert()

        return redirect(
            url_for("index")
        )  # Redirect to the homepage or wherever you want

    @app.route("/edit_movie_form/<int:movie_id>", methods=["GET"])
    # @requires_auth("update:movies")
    def edit_movie_form(movie_id):
        # movie = Movie.query.get(movie_id)
        # actors = Actor.query.all()
        # selected_actors = [actor.id for actor in movie.actors]
        return render_template("edit_movie_form.html")

    #     return jsonify({
    #         'movie': {
    #             'id': movie.id,
    #             'title': movie.title,
    #             'release_date': str(movie.release_date),
    #             'actors': [{'id': actor.id, 'name': actor.name} for actor in movie.actors]
    #         }
    # })

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

            # Include the updated movie details in the response
            return jsonify(
                {
                    "message": "Movie updated successfully",
                    "movie": {
                        "id": movie.id,
                        "title": movie.title,
                        "release_date": movie.release_date,
                        "actors": [
                            {"id": actor.id, "name": actor.name}
                            for actor in movie.actors
                        ],
                    },
                }
            )

        return jsonify({"error": "Movie not found"}), 404

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

    @app.route("/delete_movie/<int:movie_id>", methods=["POST"])
    @requires_auth("delete:movies")
    def delete_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            movie.delete()
        return redirect(
            url_for("view_movies")
        )  # Redirect to the movies page or home page

    @app.route("/delete_actor/<int:actor_id>", methods=["POST"])
    def delete_actor(actor_id):
        actor = Actor.query.get(actor_id)
        if actor:
            actor.delete()
        return redirect(url_for("actors"))  # Redirect to the actors page or home page

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
