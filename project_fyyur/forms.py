from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, Regexp

class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AN', 'AN'),
            ('AP', 'AP'),
            ('AR', 'AR'),
            ('AS', 'AS'),
            ('BR', 'BR'),
            ('CG', 'CG'),
            ('CH', 'CH'),
            ('DD', 'DD'),
            ('DH', 'DH'),
            ('DL', 'DL'),
            ('GA', 'GA'),
            ('GJ', 'GJ'),
            ('HP', 'HP'),
            ('HR', 'HR'),
            ('JH', 'JH'),
            ('JK', 'JK'),
            ('KA', 'KA'),
            ('KL', 'KL'),
            ('LA', 'LA'),
            ('LD', 'LD'),
            ('MH', 'MH'),
            ('ML', 'ML'),
            ('MN', 'MN'),
            ('MP', 'MP'),
            ('MZ', 'MZ'),
            ('NL', 'NL'),
            ('OR', 'OR'),
            ('PB', 'PB'),
            ('PY', 'PY'),
            ('RJ', 'RJ'),
            ('SK', 'SK'),
            ('TN', 'TN'),
            ('TR', 'TR'),
            ('TS', 'TS'),
            ('UK', 'UK'),
            ('UP', 'UP'),
            ('WB', 'WB'),
        
        ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website = StringField(
        'website'
    )

    seeking_talent = BooleanField( 'seeking_talent' )

    seeking_description = StringField(
        'seeking_description'
    )



class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
             ('AN', 'AN'),
            ('AP', 'AP'),
            ('AR', 'AR'),
            ('AS', 'AS'),
            ('BR', 'BR'),
            ('CG', 'CG'),
            ('CH', 'CH'),
            ('DD', 'DD'),
            ('DH', 'DH'),
            ('DL', 'DL'),
            ('GA', 'GA'),
            ('GJ', 'GJ'),
            ('HP', 'HP'),
            ('HR', 'HR'),
            ('JH', 'JH'),
            ('JK', 'JK'),
            ('KA', 'KA'),
            ('KL', 'KL'),
            ('LA', 'LA'),
            ('LD', 'LD'),
            ('MH', 'MH'),
            ('ML', 'ML'),
            ('MN', 'MN'),
            ('MP', 'MP'),
            ('MZ', 'MZ'),
            ('NL', 'NL'),
            ('OR', 'OR'),
            ('PB', 'PB'),
            ('PY', 'PY'),
            ('RJ', 'RJ'),
            ('SK', 'SK'),
            ('TN', 'TN'),
            ('TR', 'TR'),
            ('TS', 'TS'),
            ('UK', 'UK'),
            ('UP', 'UP'),
            ('WB', 'WB'),
        ]
    )
    phone = StringField(
        # Regexp from https://uibakery.io/regex-library/phone-number-python under the section
        # The more complex phone number validation
        'phone', validators=[DataRequired(), Regexp("^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$", message="Phone number provided is not accepted")]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
     )
    facebook_link = StringField(
    'facebook_link', validators=[URL(require_tld=True, message='Invalid URL. Must be a valid Facebook URL.')]
     )
    website = StringField(
        'website'
     )

    seeking_venue = BooleanField( 'seeking_venue' )

    seeking_description = StringField(
            'seeking_description'
     )

