
## todoapp

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