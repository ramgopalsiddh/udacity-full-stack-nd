from flaskr import create_app

# run with `flask run --reload` to hot reload on changes
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
