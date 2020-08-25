from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, form
from wtforms.validators import InputRequired, ValidationError
from urllib.parse import urlparse


class UrlForm(FlaskForm):

    url = StringField('url',
                     validators=[InputRequired(message="URL required")])

    def validate_url(form, url):

        url = url.data
        o = urlparse(url)
        path = o.netloc + o.path[:11]

        if path != 'www.1001tracklists.com/tracklist/':
            raise ValidationError("Not a valid URL from 1001Tracklists! Make sure the URL starts with "
                                  "'www.1001tracklists.com/tracklist/'")





