INSERT INTO
  "Venue" (
    name,
    genres,
    address,
    city,
    state,
    phone,
    website,
    facebook_link,
    image_link,
    seeking_talent,
    seeking_description
  )
VALUES
  (
    'The Musical Hop',
    'Jazz,Reggae,Swing,Classical,Folk',
    '1015 Folsom Street',
    'San Francisco',
    'CA',
    '123-123-1234',
    'https://www.themusicalhop.com',
    'https://www.facebook.com/TheMusicalHop',
    'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
    true,
    'We are on the lookout for a local artist to play every two weeks. Please call us.'
  );

INSERT INTO
  "Venue" (
    name,
    genres,
    address,
    city,
    state,
    phone,
    website,
    facebook_link,
    image_link,
    seeking_talent
  )
VALUES
  (
    'The Dueling Pianos Bar',
    'Classical,R&B,Hip-Hop',
    '335 Delancey Street',
    'New York',
    'NY',
    '914-003-1132',
    'https://www.theduelingpianos.com',
    'https://www.facebook.com/theduelingpianos',
    'https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80',
    false
  );

INSERT INTO
  "Venue" (
    name,
    genres,
    address,
    city,
    state,
    phone,
    website,
    facebook_link,
    image_link,
    seeking_talent
  )
VALUES
  (
    'Park Square Live Music & Coffee',
    'Rock n Roll,Jazz,Classical,Folk',
    '34 Whiskey Moore Ave',
    'San Francisco',
    'CA',
    '415-000-1234',
    'https://www.parksquarelivemusicandcoffee.com',
    'https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
    'https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
    false
  );

INSERT INTO
  "Venue" (
    name,
    genres,
    address,
    city,
    state,
    phone,
    website,
    facebook_link,
    seeking_talent,
    seeking_description
  )
VALUES
  (
    'The AT&T Garder',
    'Jazz,Reggae,Swing,Classical,Folk',
    '1015 King Street',
    'San Francisco',
    'CA',
    '888-999-0101',
    'https://www.theattgarden.com',
    'https://www.facebook.com/theattgarden',
    true,
    'We are on the lookout for a local artist to play every two weeks. Please call us.'
  );

-- Insert Artists
INSERT INTO
  "Artist"(
    name,
    genres,
    city,
    state,
    phone,
    website,
    facebook_link,
    seeking_venue,
    seeking_description,
    image_link
  )
VALUES
  (
    'Guns N Petals',
    'Rock n Roll',
    'San Francisco',
    'CA',
    '326-123-5000',
    'https://www.gunsnpetalsband.com',
    'https://www.facebook.com/GunsNPetals',
    true,
    'Looking for shows to perform at in the San Francisco Bay Area!',
    'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'
  );

INSERT INTO
  "Artist"(
    name,
    genres,
    city,
    state,
    phone,
    facebook_link,
    seeking_venue,
    image_link
  )
VALUES
  (
    'Matt Quevedo',
    'Jazz',
    'New York',
    'NY',
    '300-400-5000',
    'https://www.facebook.com/mattquevedo923251523',
    false,
    'https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80'
  );

INSERT INTO
  "Artist"(
    name,
    genres,
    city,
    state,
    phone,
    seeking_venue,
    image_link
  )
VALUES
  (
    'The Wild Sax Band',
    'Jazz,Classical',
    'San Francisco',
    'CA',
    '432-325-5432',
    false,
    'https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80'
  );


INSERT INTO "Show"(venue_id, artist_id, start_time) VALUES(1, 1, '2019-05-21T21:30:00.000Z');
INSERT INTO "Show"(venue_id, artist_id, start_time) VALUES(1, 1, '2020-05-21T21:30:00.000Z');
INSERT INTO "Show"(venue_id, artist_id, start_time) VALUES(3, 2, '2019-06-15T23:00:00.000Z');
INSERT INTO "Show"(venue_id, artist_id, start_time) VALUES(3, 3, '2019-04-01T20:00:00.000Z');
INSERT INTO "Show"(venue_id, artist_id, start_time) VALUES(3, 3, '2035-04-08T20:00:00.000Z');
INSERT INTO "Show"(venue_id, artist_id, start_time) VALUES(3, 3, '2035-04-15T20:00:00.000Z');


-- Query Artists with upcoming shows
SELECT artists.id, artists.name, count(shows.start_time)
FROM artists
LEFT OUTER JOIN shows ON artists.id = shows.artist_id AND shows.start_time > NOW()
GROUP BY artists.id;

-- Query Artists with past shows
SELECT artists.id, artists.name, count(shows.start_time)
FROM artists
LEFT OUTER JOIN shows ON artists.id = shows.artist_id AND shows.start_time <= NOW()
GROUP BY artists.id;


-- Query Artists with upcoming shows
SELECT artists.id, artists.name, count(shows.start_time)
FROM artists
LEFT OUTER JOIN shows ON artists.id = shows.artist_id AND shows.start_time > NOW()
GROUP BY artists.id;

-- Query Venues with upcoming shows
SELECT venues.id, venues.name, count(shows.start_time)
FROM venues
LEFT OUTER JOIN shows ON venues.id = shows.artist_id AND shows.start_time > NOW()
GROUP BY venues.id;

-- Query Venues with past shows
SELECT venues.id, venues.name, count(shows.start_time)
FROM venues
LEFT OUTER JOIN shows ON venues.id = shows.artist_id AND shows.start_time <= NOW()
GROUP BY venues.id;