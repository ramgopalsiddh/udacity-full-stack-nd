#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
# add new in changes
from flask_migrate import Migrate
import config

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
# add for migration
migrate = Migrate(app, db)

# DONE: connect to a local postgresql database

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_ECHO'] = config.SQLALCHEMY_ECHO

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    # DONE: implement any missing fields, as a database migration using Flask-Migrate
    
    # add coloum according to requirement
    genres = db.Column("genres", db.ARRAY(db.String()), nullable=False)
    website = db.Column(db.String(250))
    seeking_talent = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String(250))

    shows = db.relationship('Show', backref='venue', lazy=True)

    def __repr__(self):
      return f"<Venue {self.id} name: {self.name}>"

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column("genres", db.ARRAY(db.String()), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
   # DONE: implement any missing fields, as a database migration using Flask-Migrate
   
   # add coloum according to requirement
    shows = db.relationship('Show', backref='artist', lazy=True)

    def __repr__(self):
      return f"<Artis {self.id} name: {self.name}>"

# DONE: Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# add show class
class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
      return f"<Show {self.id}, Artist {self.artist_id}, Venue {self.venue_id}>"

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#
 # format datetime
def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')

#-----------------------------------------------------------------------------------------------------
#  Venues
#  -----------------------------------------------------------------------------------------------------

@app.route('/venues')
def venues():
  # DONE: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

  #update according to requirement
  data = []
  # get all venues
  venues = Venue.query.all()

  # Use set so there are no duplicate venues
  locations = set()

  for venue in venues:
    # add city / state tuples
    locations.add((venue.city, venue.state))

  # for each unique city / state, add veneus
  for location in locations:
    data.append({
      "city": location[0],
      "state": location[1],
      "venues": []
    })

  for venue in venues:
    num_upcoming_shows = 0

    shows = Show.query.filter_by(venue_id=venue.id).all()
    # get current date to filter num_upcoming_shows
    current_date = datetime.now()

    for show in shows:
      if show.start_time > current_date:
        num_upcoming_shows += 1
    

    for venue_location in data:
      if venue.state == venue_location['state'] and venue.city == venue_location['city']:
        venue_location['venues'].append({
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": num_upcoming_shows
        })

  return render_template('pages/venues.html', areas=data);


@app.route('/venues/search', methods=['POST'])
def search_venues():
  # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  #update according to requirement for "search operation"
  search_term = request.form.get('search_term', '')
  result = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))

  response={
    "count": result.count(),
    "data": result
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))



@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # DONE: replace with real venue data from the venues table, using venue_id

  #update according to requirement for "show venue operation"
  venue = Venue.query.get(venue_id)
  shows = Show.query.filter_by(venue_id=venue_id).all()
  past_shows = []
  upcoming_shows = []
  current_time = datetime.now()

  for show in shows:
    data = {
          "artist_id": show.artist_id,
          "artist_name": show.artist.name,
           "artist_image_link": show.artist.image_link,
           "start_time": format_datetime(str(show.start_time))
        }
    if show.start_time > current_time:
      upcoming_shows.append(data)
    else:
      past_shows.append(data)

  data={
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description":venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows)
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

 #update according to requirement for "create venue operation"
  try:
    # get form data and create
    form = VenueForm(request.form)
    venue = Venue(name=form.name.data, city=form.city.data, state=form.state.data, address=form.address.data,
                  phone=form.phone.data, image_link=form.image_link.data, genres=form.genres.data,
                  facebook_link=form.facebook_link.data, seeking_description=form.seeking_description.data,
                  website=form.website.data, seeking_talent=form.seeking_talent.data)
    # coomit session to database
    #logging.debug("creating venues:", form, venue)
    db.session.add(venue)
    # import pdb; pdb.set_trace()
    db.session.commit()
    # flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    # catches errors
    db.session.rollback()
    flash('An error occurred. Venue'+ request.form['name'] + ' could not be listed')
  finally:
    # closes session
    db.session.close()

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

 #update according to requirement for "delete venue operation"
  try:
    # Get venue by ID
    venue = Venue.query.get(venue_id)
    venue_name = venue.name

    db.session.delete(venue)
    db.session.commit()

    flash('Venue ' + venue_name + ' was deleted')
  except:
    flash(' an error occured and Venue ' + venue_name + ' was not deleted')
    db.session.rollback()
  finally:
    db.session.close()

  return redirect(url_for('index'))


#---------------------------------------------------------------------------------------------------
#  Artists
#  -------------------------------------------------------------------------------------------------
@app.route('/artists')
def artists():
  # DONE: replace with real data returned from querying the database

  #update according to requirement for "artists home route"
  data = []
  
  artists = Artist.query.all()
  for artist in artists:
    data.append({
      "id": artist.id,
      "name": artist.name
    })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".

  #update according to requirement for "search artists route"
  search_term = request.form.get('search_term', '')

  # filter artists by case insensitive search
  result = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))

  response = {
    'count': result.count(),
    'data': result
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # DONE: replace with real artist data from the artist table, using artist_id

  #update according to requirement for "show artists route"
  artist = Artist.query.get(artist_id)
  shows = Show.query.filter_by(artist_id=artist_id).all()
  past_shows = []
  upcoming_shows = []
  current_time = datetime.now()
  # filter shows by upcoming and past

  for show in shows:
    data = {
      'venue_id': show.venue_id,
      'venue_name': show.venue.name,
      'venue_image_link': show.venue.image_link,
      'start_time': format_datetime(str(show.start_time))
    }
    if show.start_time > current_time:
      upcoming_shows.append(data)
    else:
      past_shows.append(data)

  data = {
    'id': artist.id,
    'name': artist.name,
    'genres': artist.genres,
    'city': artist.city,
    'state': artist.state,
    'phone': artist.phone,
    'facebook_link': artist.facebook_link,
    'image_link': artist.image_link,
    'past_shows': past_shows,
    'upcoming_shows': upcoming_shows,
    'past_shows_count': len(past_shows),
    'upcoming_shows_count': len(upcoming_shows)
  }

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
# DONE: populate form with fields from artist with ID <artist_id>

#update according to requirement for "edit artists route"
  artist = Artist.query.get(artist_id)
  form = ArtistForm(obj=artist)

  # artist_data={
  #   "id": artist.id,
  #   "name": artist.name,
  #   "genres": artist.genres,
  #   "city": artist.city,
  #   "state": artist.state,
  #   "phone": artist.phone,
  #   "facebook_link": artist.facebook_link,
  #   "image_link": artist.image_link
  # }

  return render_template('forms/edit_artist.html', form=form, artist_id=artist_id)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # DONE: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

 #update according to requirement for " submit edit artists route"
  try:
      form = ArtistForm(request.form)
      artist = Artist.query.get(artist_id)
      
      artist.name = form.name.data
      artist.phone = form.phone.data
      artist.state = form.state.data
      artist.city = form.city.data
      artist.genres = form.genres.data
      artist.image_link = form.image_link.data
      artist.facebook_link = form.facebook_link.data

      #import pdb; pdb.set_trace()

      db.session.commit()
      flash('The Artist ' + request.form['name'] + ' has been successfully updated!')
  except:
      db.session.rollback()
      flash('An Error has occured and the update unsucessful')
  finally:
      db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))


#-----------------------------------------------------------------------------------------------------
# Venues
#  ----------------------------------------------------------------------------------------------------

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):  
  venue = Venue.query.get(venue_id)
  form = VenueForm(obj=venue)

  return render_template('forms/edit_venue.html', form=form, venue_id=venue_id)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # DONE: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

#update according to requirement for "submit edited venue route"
  try:
    form = VenueForm(request.form)
    venue = Venue.query.get(venue_id)

    venue.name = form.name.data
    venue.genres = form.genres.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    venue.facebook_link = form.facebook_link.data
    venue.website = form.website.data
    venue.image_link = form.image_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data

    db.session.commit()
    flash('Venue ' + form.name.data + ' has been updated')
  except:
    db.session.rollback()
    flash('An error occured while trying to update Venue')
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ---------------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # DONE: insert form data as a new Venue record in the db, instead
  # DONE: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')


#update according to requirement for "created artist submission route"
  try:
    form = ArtistForm(request.form)
    artist = Artist(name=form.name.data, city=form.city.data, state=form.state.data,
                    phone=form.phone.data, genres=form.genres.data,
                    image_link=form.image_link.data, facebook_link=form.facebook_link.data)
    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    db.session.rollback()
    flash('An error ocurred, Artist ' + request.form['name'] + ' could not be listed')
  finally:
    db.session.close()
  return render_template('pages/home.html')


# Add delete artist route for "delete artist"
@app.route('/artist/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  try:
    artist = Artist.query.get(artist_id)
    artist_name = artist.name

    db.session.delete(artist)
    db.session.commit()

    flash('Artist ' + artist_name + ' was deleted')
  except:
    flash('An error occured and Artist ' + artist_name + ' was not deleted')
    db.session.rollback()

  finally:
    db.session.close()
  return redirect(url_for('index'))


# -----------------------------------------------------------------------------------------------
#  Shows
# -----------------------------------------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # DONE: replace with real venues data.

  #update according to requirement for "display show route"
  shows = Show.query.order_by(db.desc(Show.start_time))

  data = []
  for show in shows:
    data.append({
      'venue_id': show.venue_id,
      'venue_name': show.venue.name,
      'artist_id': show.artist_id,
      'artist_name': show.artist.name,
      'artist_image_link': show.artist.image_link,
      'start_time': format_datetime(str(show.start_time))
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # DONE: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  # DONE: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

  #update according to requirement for "submit show route"
  try:
    show = Show(artist_id=request.form['artist_id'], venue_id=request.form['venue_id'],
                start_time=request.form['start_time'])

    db.session.add(show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  
  except:
    db.session.rollback()
    flash('An error occured. show could not be listed')
  finally:
    db.session.close()


  return render_template('pages/home.html')

# error handler
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()
    

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''