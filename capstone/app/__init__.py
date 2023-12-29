from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session,
    make_response,
)
from flask_cors import CORS
from models import db, Config, Movie, Actor
from flask_migrate import Migrate
from auth.auth import requires_auth, AuthError
import secrets

migrate = Migrate()


class NotFoundError(Exception):
    def __init__(self):
        self.error = "not found"
        self.status_code = 404


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = secrets.token_hex(16)

    # Configure database
    app.config.from_object(Config)
    app.config["SQLALCHEMY_ECHO"] = True

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
    def main():
        auth_token = request.cookies.get("auth_token")
        if auth_token:
            # User is logged in
            return render_template("index.html", logged_in=True)
        else:
            # User is logged out
            return render_template("index.html", logged_in=False)

    # logout
    @app.route("/logout")
    def logout():
        # Clear the session and any other user-related data
        session.clear()
        # Redirect to the Auth0 logout URL
        response = make_response(
            redirect(
                "https://ramgopalsiddh.us.auth0.com/logout?client_id=nGfqDFBy34G83Nffy4CyajPMMb8hX31Y&returnTo="
                + url_for("main", _external=True)
            )
        )
        response.delete_cookie("auth_token")

        return response

    @app.route("/movies", methods=["GET"])
    @requires_auth("view:movies")
    def movies(payload):
        movies = Movie.query.order_by(Movie.id).all()
        movies = list(map(lambda movie: movie.format(), movies))
        return jsonify({"success": True, "movies": movies})
        # movies_data = Movie.query.all()
        # return render_template("movies.html", movies=movies_data)

    @app.route("/view-movies", methods=["GET"])
    def view_movies():
        return render_template("movies.html")

    # Route for displaying actors
    @app.route("/actors", methods=["GET"])
    @requires_auth("view:actors")
    def actors(payload):
        actors = Actor.query.order_by(Actor.id).all()
        actors = list(map(lambda actor: actor.format(), actors))
        return jsonify({"success": True, "actors": actors})

    @app.route("/view-actors", methods=["GET"])
    def view_actors():
        return render_template("actors.html")

    @app.route("/create_movie_form", methods=["GET"])
    def create_movie_form():
        # actors_data = Actor.query.all()
        return render_template("create_movie_form.html")

    # Route for handling the submission of the "Create Movie" form
    @app.route("/create_movie", methods=["POST"])
    @requires_auth("post:movies")
    def create_movie(payload):
        try:
            data = request.get_json()

            title = data.get("title")
            release_date = data.get("release_date")
            actor_ids = data.get("actors")

            if not title or not release_date:  # or not actor_ids:
                return jsonify({"error": "Please fill out all required fields."}), 400

            new_movie = Movie(title=title, release_date=release_date)
            for actor_id in actor_ids:
                actor = Actor.query.get(actor_id)
                if actor:
                    new_movie.actors.append(actor)

            new_movie.insert()

            return jsonify({"message": "Movie created successfully!"}), 201
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    # Route for displaying the "Create Actor" form
    @app.route("/create_actor_form")
    def create_actor_form():
        return render_template("create_actor_form.html")

    # Route for handling the submission of the "Create Actor" form
    @app.route("/create_actor", methods=["POST"])
    @requires_auth("post:actors")
    def create_actor(payload):
        try:
            data = request.get_json()

            name = data.get("name")
            age = data.get("age")
            gender = data.get("gender")
            movie_ids = data.get("movie_ids")

            if (
                not name or not age or not gender or not movie_ids
            ):  # Add more conditions if needed
                return jsonify({"error": "Please fill out all required fields."}), 400

            movie_ids_set = set([int(movie_id) for movie_id in movie_ids.split(",")])
            # Query the movies with the specified IDs
            movies = Movie.query.filter(Movie.id.in_(movie_ids_set)).all()

            fetched_movie_ids_set = set([movie.id for movie in movies])

            # Ensure that the lists are the same
            if fetched_movie_ids_set == movie_ids_set:
                pass
                # print("The lists are the same.")
            else:
                # print("The lists are different.")
                # Find the difference between the lists
                difference = movie_ids_set - fetched_movie_ids_set
                # print("Difference:", list(difference))
                return jsonify(
                    {"error": "Some movie ids are invalid: {}".format(difference)}
                ), 400

            new_actor = Actor(name=name, age=age, gender=gender)
            new_actor.movies.extend(movies)

            new_actor.insert()

            return jsonify({"message": "Actor created successfully!"}), 201
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    @app.route("/get_movie_data/<int:movie_id>", methods=["GET"])
    @requires_auth("view:movies")
    def get_movie_data(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            raise NotFoundError

        actors = Actor.query.all()
        if not actors:
            raise NotFoundError

        # return jsonify return json data in "/edit_movie_form/<int:movie_id>" Route
        return jsonify(
            {
                "movie": {
                    "id": movie.id,
                    "title": movie.title,
                    "release_date": str(movie.release_date),
                    "actors": [
                        {"id": actor.id, "name": actor.name} for actor in movie.actors
                    ],
                },
                "actors": list(map(lambda movie: movie.format(), actors)),
            }
        )

   # this use in edit movie form for populate all actors name
    @app.route("/get_actors_data", methods=["GET"])
    @requires_auth("view:actors")
    def get_actors_data(payload):
        try:
            # Query all actors
            actors = Actor.query.all()

            # Convert actors to a list of dictionaries
            actors_list = [{"id": actor.id, "name": actor.name} for actor in actors]

            # Return the list of actors as JSON
            return jsonify({"actors": actors_list})
        except Exception as e:
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    # this use for print specfic actor's data in edit actor form
    @app.route("/get_actor/<int:actor_id>", methods=["GET"])
    @requires_auth("view:actors")
    def get_actors(payload, actor_id):
            # Query for get actor by id
            actor = Actor.query.get(actor_id)
            if not actor:
                raise NotFoundError

            movies = Movie.query.all()
            if not movies:
                raise NotFoundError
            # return jsonify return json data in "/edit_movie_form/<int:movie_id>" Route
            return jsonify(
                {
                    "actor": {
                        "id" : actor.id,
                        "name": actor.name,
                        "age": actor.age,
                        "gender": actor.gender,
                        "movies": [
                            {"id": movie.id, "title": movie.title} for movie in actor.movies
                        ],
                    },
                    "movies": list(map(lambda actor: actor.format(), movies)),
                }
            )


    # render edit movie template
    @app.route("/edit_movie_form/<int:movie_id>", methods=["GET"])
    def edit_movie_form(movie_id):
        # Render an HTML template with the JSON data
        return render_template("edit_movie_form.html", movie_id=movie_id)

    @app.route("/edit_movie/<int:movie_id>", methods=["POST"])
    @requires_auth("update:movies")
    def edit_movie(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if not movie:
            raise NotFoundError

        data = request.json  # Use request.json to parse JSON data
        title = data.get("title")
        release_date = data.get("release_date")
        actors_ids = data.get("actors")
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
                        {"id": actor.id, "name": actor.name} for actor in movie.actors
                    ],
                },
            }
        )

    @app.route("/edit_actor_form/<int:actor_id>")
    def edit_actor_form(actor_id):
        # actor = Actor.query.get(actor_id)
        # movie_ids = [movie.id for movie in actor.movies] if actor.movies else []
        return render_template("edit_actor_form.html", actor_id=actor_id)

    @app.route("/edit_actor/<int:actor_id>", methods=["POST"])
    @requires_auth("update:actors")
    def edit_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if not actor:
            raise NotFoundError

        data = request.json  # Use request.json to parse JSON data
        name = data.get("name")
        age = data.get("age")
        gender = data.get("gender")
        movie_ids = data.get("movie_ids")

        if (
            not name or not age or not gender or not movie_ids
        ):  # Add more conditions if needed
         return jsonify({"error": "Please fill out all required fields."}), 400

        movie_ids_set = set([int(movie_id) for movie_id in movie_ids.split(",")])
            # Query the movies with the specified IDs
        movies = Movie.query.filter(Movie.id.in_(movie_ids_set)).all()

        fetched_movie_ids_set = set([movie.id for movie in movies])

            # Ensure that the lists are the same
        if fetched_movie_ids_set == movie_ids_set:
            pass
                # print("The lists are the same.")
        else:
                # print("The lists are different.")
                # Find the difference between the lists
            difference = movie_ids_set - fetched_movie_ids_set
                # print("Difference:", list(difference))
            return jsonify(
                {"error": "Some movie ids are invalid: {}".format(difference)}
            ), 400

        actor.name = name
        actor.age = age
        actor.gender = gender
        actor.movies.extend(movies)

        actor.update()

        # Include the updated movie details in the response
        return jsonify(
            {
                "message": "Actor updated successfully",
                "actor": {
                    "id": actor.id,
                    "name": actor.name,
                    "age": actor.age,
                    "gender": actor.gender,
                    "movies": [
                        {"id": movie.id, "title": movie.title} for movie in actor.movies
                    ],
                },
            }
        )


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
    @requires_auth("delete:actors")
    def delete_actor(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if actor:
            actor.delete()
        return redirect(url_for("view_actors"))  # Redirect to the actors page or home page

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    @app.errorhandler(NotFoundError)
    def handle_not_found_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


app = create_app()

if __name__ == "__main__":
    app.run()
