
# todoapp

# YouTube video link 
 - ### Project's YouTube video link :- https://youtu.be/FMWkbzpMM1c

## screenshots 

### HOME
  <img src="screenshot/home.png"/>

### Create a new list
  <img src="screenshot/create_new_list_1.png"/>
  <img src="screenshot/create_new_list_2.png"/>

### Create new todo
  <img src="screenshot/create_new_todo_1.png"/>
  <img src="screenshot/create_new_todo_2.png"/>
  <img src="screenshot/create_new_todo_3.png"/>

### Delete a todo
  <img src="screenshot/delete_todo.png"/>

### Delete a list
  <img src="screenshot/delete_list.png"/>

### Mark complete a todo
  <img src="screenshot/complete_todo.png"/>

### Home after all operation(modification)
  <img src="screenshot/home_after_all_modificatoin.png"/>



tech stack used

- Python 3
- Flask
- PostgresSQL
- psycopg2
- SQLAlchemy
- Flask-SQLAlchemy


## Install psycopg2

We will install psycopg2 and use it to establish a connection to our postgres server, and interact with it in python.

#### psycopg2 installation steps
Follow the psycopg2 install instructions found here.

Install Tips:

Make sure you have Python 3 version between 3.4 to 3.7. You can find out with
`$ python --version`
Use the latest pip version: `$ pip3 install -U pip`
Replace X.Y in the export PATH... line with the version of Postgres you are using. Find out with $ postgres -V. E.g.:
`$ postgres -V`
`postgres (PostgreSQL) 10.2`

If the version is 10.2, then replace the X.Y in the export PATH line with 10.2: In ~/.bash_profile or ~/.bashrc, we should add:

`export PATH=/usr/lib/postgresql/10.2/bin/:$PATH`
To export and add things to your PATH, add the export PATH=.... line to either ~/.bashrc or ~/.bash_profile on your machine, e.g. with gedit:
`$ gedit ~/.bashrc`

`$ gedit ~/.bash_profile`

When you are done editing your bash profile, be sure to run source ~/.bash_profile or source ~/.bashrc on your edited file, so your terminal session can grab the latest profile changes.
After editing your bash profile, you are ready to run the install step:

`$ pip install pyscopg2`
A prerequisite for psycopg2 is OpenSSL. If you try installing and run into error ld: library not found for -lssl, then install openssl first.

Don't forget to run `source ~/.bash_profile` or `source ~/.profile` when done.
If the regular install doesn't work, you can also just install the binary version instead:

`pip install psycopg2-binary` which replaces the need to run pip install pyscopg2

Install troubleshooting threads:
- For error Failed building wheel for psycopg2: https://stackoverflow.com/questions/34304833/failed-building-wheel-for-psycopg2-macosx-using-virtualenv-and-pip

- For error pg_config executable not found: https://stackoverflow.com/questions/11618898/pg-config-executable-not-found


## Installing Flask-Migrate
  Do a pip install of Flask-Migrate, or if you're using a custom Python 3, Python version you could do pip three install Flask-Migrate to install it for Python 3.

 - Next, install Flask-Migrate by running:

   `pip3 install Flask-Migrate`
___
#### todoapp/app.py At the top of your code, modify as follows

- from flask_migrate import Migrate
- app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abc@localhost:5432/todoapp'
- db = SQLAlchemy(app)
- migrate = Migrate(app, db)
---

### Follow along! Interactive Workspace
 - Install Flask-Migrate
 - Instantiate migrate using the code above
 #### NOTE:

 You will need to install flask_migrate
  `pip install flask_migrate`
 (and possibly if needed) reinstall `pip install flask_alchemy`
 You will need to modify the code at the top of your app.py page, changing postgres:// to postgresql:// as shown below

  - app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abc@localhost:5432/todoapp'
---
---
- Creating the migrations directory structure using 
`flask db init`

- Terminal

`cd todoapp`     (if you are not already there)
`flask db init`

- Syncing models using 
  `flask db migrate`

remove or comment out the "db.create_all()" command from todo/app.y

- Terminal

   - (continuing from previous code demo above)

- (make sure you are in the todoapp folder)
- `sudo -u postgres -i`
- `dropdb todoapp`
- `createdb todoapp`
- `exit`
- `flask db migrate`


#### Walk-Throughs
`flask db upgrade` and `flask db downgrade`
- `flask db upgrade`
Let's go ahead and run `flask db upgrade`, and this went ahead and applied that migration with

this particular revision ID. That comes from the revision ID in our migration file. So now that we run this migration, we should see this table exists in our database using the `psql todoapp` command.

We not only see that "todos" table exists here, but we also see another table called "alembic version", which stores the versions of our database, and is generally an internally use table that we should generally not touch, as it manages all of our migrations and database versions for us.

- In Terminal

`flask db migrate`

then

`flask db upgrade`

