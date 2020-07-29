from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


TESTING = True
DEBUG = True
FLASK_ENV = 'development'
SPOTIFY_CLIENT_ID = environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = environ.get('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = environ.get('SPOTIFY_REDIRECT_URI')
MONGO_URI = environ.get('MONGO_URI')
