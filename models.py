from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
  __tablename__ = 'Venue'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  address = db.Column(db.String(120))
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  facebook_link = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  # New Fields
  genres = db.Column(db.String)
  website = db.Column(db.String()) # New Field
  seeking_talent = db.Column(db.Boolean, default=False)
  seeking_description = db.Column(db.String(500))

  def add(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @property
  def serialize(self):
    return {
      'id': self.id,
      'name': self.name,
      'address': self.address,
      'city': self.city,
      'state': self.state,
      'phone': self.phone,
      'facebook_link': self.facebook_link,
      'image_link': self.image_link,
      # New Fields
      'genres': self.genres.split(','),
      'website': self.website,
      'seeking_talent': self.seeking_talent,
      'seeking_description': self.seeking_description
    }

  @property
  def serialize_upcoming_shows_details(self):
    return {
      'upcoming_shows': [
        show.serialize_with_artist_venue for show in Show.query.filter(
          Show.start_time > datetime.now(),
          Show.venue_id == self.id
        ).all()
      ],
      'upcoming_shows_count': len(Show.query.filter(
        Show.start_time > datetime.now(),
        Show.venue_id == self.id
      ).all())
    }

  @property
  def serialize_past_shows_details(self):
    return {
      'past_shows': [
        show.serialize_with_artist_venue for show in Show.query.filter(
          Show.start_time < datetime.now(),
          Show.venue_id == self.id
        ).all()
      ],
      'past_shows_count': len(Show.query.filter(
        Show.start_time < datetime.now(),
        Show.venue_id == self.id
      ).all())
    }

  @property
  def serialize_venues_group_by_city_state(self):
    return {
      'city': self.city,
      'state': self.state,
      'venues': [
        {
          **v.serialize,
          'num_upcoming_shows': v.serialize_upcoming_shows_details['upcoming_shows_count']
        } for v in Venue.query.filter(
          Venue.city == self.city,
          Venue.state == self.state
        ).all()
      ]
    }


class Artist(db.Model):
  __tablename__ = 'Artist'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  address = db.Column(db.String(120))
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  # New Fields
  website = db.Column(db.String(500))
  seeking_venue = db.Column(db.Boolean)
  seeking_description = db.Column(db.String(500))

  # DONE: TODO: implement any missing fields, as a database migration using Flask-Migrate

  def update(self):
    db.session.commit()

  @property
  def serialize(self):
    return {
      'id': self.id,
      'name': self.name,
      'address': self.address,
      'city': self.city,
      'phone': self.phone,
      'genres': self.genres.split(','),
      'image_link': self.image_link,
      'facebook_link': self.facebook_link,
      'website': self.website,
      'seeking_venue': self.seeking_venue,
      'seeking_description': self.seeking_description
    }

  @property
  def serialize_past_shows_details(self):
    past_shows = Show.query.filter(
          Show.start_time < datetime.now(),
          Show.artist_id == self.id
        ).all()
    return {
      'past_shows_count': len(past_shows),
      'past_shows': [
        show.serialize_with_artist_venue for show in past_shows
      ]
    }

  @property
  def serialize_upcoming_shows_details(self):
    upcoming_shows = Show.query.filter(
          Show.start_time > datetime.now(),
          Show.artist_id == self.id
        ).all()
    return {
      'upcoming_shows_count': len(upcoming_shows),
      'upcoming_shows': [
        show.serialize_with_artist_venue for show in upcoming_shows
      ]
    }

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
  __tablename__ = "Show"
  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime, nullable=False)
  # Show-Venue relationship
  venue_id = db.Column(db.Integer,  db.ForeignKey('Venue.id'), nullable=False)
  venue = db.relationship('Venue', backref=db.backref('shows', cascade='all, delete'))
  # Show-Artist relationship
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  artist = db.relationship('Artist', backref=db.backref('shows', cascade='all, delete'))

  @property
  def serialize(self):
    return {
      'id': self.id,
      'start_time': self.start_time.strftime('%m/%d/%Y, %H:%M:%S'),
      'venue_id': self.venue_id,
      'artist_id': self.artist_id,
      'venue_image_link': self.venue.image_link,
      'artist_image_link': self.artist.image_link
    }

  @property
  def serialize_with_artist_venue(self):
    show_data = self.serialize
    # venue = Venue.query.filter(Venue.id == self.venue_id).one_or_none()
    # artist = Artist.query.filter(Artist.id == self.artist_id).one_or_none()
    return {
      **show_data,
      'venue': self.venue.serialize, # venue.serialize if venue is not None else None,
      'artist': self.artist.serialize # if artist is not None else None
    }