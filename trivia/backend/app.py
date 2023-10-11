from flaskr import create_app

# run with `python3 app.py`
#
# `flask run --debug` will not work correctly.
# or you can run it with the following command:
# FLASK_APP="flaskr:create_app('<correct database path>')" flask run --debug
# see more: https://www.twilio.com/blog/how-run-flask-application
if __name__ == '__main__':
    database_name = 'trivia'
    database_path = 'postgresql://ram@localhost:5432/{}'.format(database_name)

    app = create_app(database_path, db_log=True)
    app.run(debug=True)
