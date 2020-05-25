#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import db, Artist, Venue, Show
import sys
from flask_wtf.csrf import CSRFProtect

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
csrf = CSRFProtect(app)

# Connect SQLAlchemy and Flask App
db.init_app(app)

# Setup Flask db migration
migrate = Migrate(app, db)
# DONE: TODO: connect to a local postgresql database


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # DONE: TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  city_states = Venue.query.distinct(Venue.city, Venue.state).all()
  data = [
    cs.serialize_venues_group_by_city_state for cs in city_states
  ]
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # DONE: TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term')
  venues = Venue.query.filter(Venue.name.ilike("%{}%".format(search_term))).all()
  response={
    "count": len(venues),
    "data": [
      v.serialize for v in venues
    ]
  }
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # DONE: TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.filter(Venue.id == venue_id).one_or_none()
  if (venue is None):
    abort(404)

  venue_data = venue.serialize
  upcoming_shows_data = venue.serialize_upcoming_shows_details_using_join
  past_shows_data = venue.serialize_past_shows_details_using_join
  # Merge Venue and Shows Data
  data = {**venue_data, **upcoming_shows_data, **past_shows_data}
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # DONE: TODO: insert form data as a new Venue record in the db, instead
  # DONE: TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  venue_form = VenueForm(request.form)

  try:
    newVenue = Venue(
      name = venue_form.name.data,
      address = venue_form.address.data,
      city = venue_form.city.data,
      state = venue_form.state.data,
      phone = venue_form.phone.data,
      facebook_link = venue_form.facebook_link.data,
      image_link = venue_form.image_link.data,
      genres = ",".join(venue_form.genres.data),
      seeking_talent = venue_form.seeking_talent.data == 'True'
    )
    newVenue.add()
    flash('Venue ' + newVenue.name + ' was successfully listed!')
    return redirect(url_for('index'))
  except:
  # DONE: TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    flash('An error occurred. Venue ' + venue_form.name.data + ' could not be listed.')
    print(sys.exc_info())
    return render_template('forms/new_venue.html', form=venue_form)

@app.route('/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # DONE: TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    delete_venue = Venue.query.filter(Venue.id == venue_id).one_or_none()
    if delete_venue is None:
      abort(400)
    else:
      delete_venue.delete()
      flash("Venue {0} has been deleted successfully".format(delete_venue.name))
  except:
    abort(400)
  # DONE: BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # DONE: TODO: replace with real data returned from querying the database
  data = [ artist.serialize for artist in Artist.query.all() ]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # DONE: TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term')
  artists = Artist.query.filter(
    Artist.name.ilike("%{}%".format(search_term))
  ).all()

  response={
    "count": len(artists),
    "data": [
      artist.serialize for artist in artists
    ]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # DONE: TODO: replace with real venue data from the venues table, using venue_id
  artist = Artist.query.filter(Artist.id == artist_id).one_or_none()
  past_shows_data = artist.serialize_past_shows_details_using_join
  upcoming_shows_data = artist.serialize_upcoming_shows_details_using_join
  if artist is not None:
    data = {
      **artist.serialize,
      **past_shows_data,
      **upcoming_shows_data
    }
    return render_template('pages/show_artist.html', artist=data)
  else:
    return redirect(url_for('artists'))

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.filter(Artist.id == artist_id).one_or_none()
  #DONE: TODO: populate form with fields from artist with ID <artist_id>
  if artist is not None:
    artistData = artist.serialize
    form.name.data = artistData.get('name')
    form.city.data = artistData.get('city')
    form.state.data = artistData.get('state')
    form.address.data = artistData.get('address')
    form.phone.data = artistData.get('phone')
    form.genres.data = artistData.get('genres')
    # form.website.data = artistData.get('website')
    form.image_link.data = artistData.get('image_link')
    form.facebook_link.data = artistData.get('facebook_link')
    # form.seeking_venue.data = "True" if artistData.get('seeking_venue') == True else "False"
    # form.seeking_description.data = artistData.get('seeking_description')
    form.image_link.data = artistData.get('image_link')

    return render_template('forms/edit_artist.html', form=form, artist=artistData)
  else:
    return redirect(url_for('artists'))


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  artist = Artist.query.filter(Artist.id == artist_id).one()
  # DONE: TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  artist_form = ArtistForm(request.form)
  if not artist_form.validate():
    return render_template('forms/edit_artist.html', form=artist_form, artist=artist)

  artist.name = artist_form.name.data
  artist.city = artist_form.city.data
  artist.state = artist_form.state.data
  artist.address =artist_form.address.data
  artist.genres = ",".join(artist_form.genres.data)
  artist.phone = artist_form.phone.data
  artist.facebook_link = artist_form.facebook_link.data
  artist.image_link = artist_form.image_link.data

  artist.update()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venueObj = Venue.query.filter(Venue.id == venue_id).one_or_none()
  if venueObj is not None:
    venue = venueObj.serialize
    form.name.data = venue['name']
    form.city.data = venue['city']
    form.state.data = venue['state']
    form.address.data = venue['address']
    form.phone.data = venue['phone']
    form.image_link.data = venue['image_link']
    form.genres.data = venue['genres']
    form.facebook_link.data = venue['facebook_link']
    form.seeking_talent.data = venue['seeking_talent']

  # DONE: TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)
  else:
    return redirect(url_for('venues'))

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # DONE: TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  venueForm = VenueForm(request.form)
  venue = Venue.query.filter(Venue.id == venue_id).one_or_none()
  try:
    venue.name = venueForm.name.data
    venue.address = venueForm.address.data
    venue.city = venueForm.city.data
    venue.state = venueForm.state.data
    venue.phone = venueForm.phone.data
    venue.facebook_link = venueForm.facebook_link.data
    venue.genres = ",".join(venueForm.genres.data)
    venue.image_link = venueForm.image_link.data

    db.session.commit()

    flash('Venue ' + request.form['name'] + ' was successfully updated!')
    return redirect(url_for('show_venue', venue_id=venue_id))
  except:
    db.session.rollback()
    flash('Failed to update venue ' + request.form['name'])

  return render_template('forms/edit_venue.html', form=venueForm, venue=venue)



#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # DONE: TODO: insert form data as a new Venue record in the db, instead
  # DONE TODO: modify data to be the data object returned from db insertion
  artistForm = ArtistForm(request.form)
  try:
    artist = Artist(
      name = artistForm.name.data,
      address = artistForm.address.data,
      city = artistForm.city.data,
      state = artistForm.state.data,
      phone = artistForm.phone.data,
      genres = ",".join(artistForm.genres.data),
      image_link = artistForm.image_link.data,
      facebook_link = artistForm.facebook_link.data
    )

    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return redirect(url_for('index'))
  except:
    # DONE: TODO: on unsuccessful db insert, flash an error instead.
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    print(sys.exc_info())
    return render_template('forms/new_artist.html', form=artistForm)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # DONE: TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = [
    show.serialize for show in Show.query.all()
  ]

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  form.artist.choices = [
    (artist.id, artist.name) for artist in Artist.query.all()
  ]
  form.venue.choices = [
    (venue.id, venue.name) for venue in Venue.query.all()
  ]
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # DONE: TODO: insert form data as a new Show record in the db, instead
  showForm = ShowForm(request.form)
  try:
    show = Show(
      start_time = showForm.start_time.data,
      venue_id = showForm.venue.data,
      artist_id = showForm.artist.data
    )

    db.session.add(show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')
    return redirect(url_for('index'))
  except:
    db.session.rollback()
    # DONE: TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

  return render_template('forms/new_show.html', form=showForm)

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
