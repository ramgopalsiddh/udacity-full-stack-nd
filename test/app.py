from flask import Flask

app = Flask(__name__)

# Define your routes and other Flask app setup here
@app.route("/")
def hello():
    return "hello welcome in Movies"

@app.route("/about")
def about():
    return "This is the about page"

@app.route("/movies")
def list_movies():
    return "List of movies: Movie 1, Movie 2, Movie 3"

if __name__ == "__main__":
    app.run()
