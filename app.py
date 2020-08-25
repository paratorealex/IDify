import tekore as tk
import os
from flask import Flask, request, redirect, session, render_template, url_for
from webscrape import getTracks
from pymongo import MongoClient
from form_model import UrlForm


conf = tk.config_from_environment()
cred = tk.Credentials(*conf)
spotify = tk.Spotify()


users = {}

def app_factory() -> Flask:
    app = Flask(__name__, template_folder="templates")
    app.config['SECRET_KEY'] = os.environ.get('TEKORE_KEY')

    client = MongoClient(os.environ.get('MONGO_URI'))
    db = client['song_db']
    collection = db['songs']

    @app.route('/', methods=['GET'])
    def main():
        return render_template('home.html')

    @app.route('/userhome', methods=['GET', 'POST'])
    def main2():

        form = UrlForm()

        if form.validate_on_submit():

            url = form.url.data

            user = session.get('user', None)

            if user is not None:
                token = users[user]

                if token.is_expiring:
                    token = cred.refresh(token)
                    users[user] = token

                try:
                    with spotify.token_as(users[user]):
                        track_uris, title = get_set_tracks(url, collection)
                        pl = spotify.playlist_create(user_id=user,
                                                     name=title,
                                                     public=False,
                                                     description='Created by Idify!')

                        spotify.playlist_add(pl.id, uris=track_uris)
                        return redirect('/created', 307)

                except Exception as e:
                    page = '<h1> Error has occurred </h1>'
                    page += f'<h1> {str(e)} </h1>'
                    return page

        return render_template('user_home.html', form=form)

    @app.route('/giveurl', methods=['GET'])
    def get_url():
        return redirect('/created')

    @app.route('/about', methods=['GET'])
    def get_about():
       return render_template('about.html')

    @app.route('/created', methods=['GET', 'POST'])
    def playlist_create():
        return render_template('created.html')

    @app.route('/login', methods=['GET'])
    def login():
        auth_url = cred.user_authorisation_url(scope=tk.scope.every)
        return redirect(auth_url, 307)


    @app.route('/callback', methods=['GET'])
    def login_callback():
        code = request.args.get('code', None)

        token = cred.request_user_token(code)
        with spotify.token_as(token):
            info = spotify.current_user()

        session['user'] = info.id
        users[info.id] = token

        return redirect('/userhome', 307)

    @app.route('/logout', methods=['GET'])
    def logout():
        uid = session.pop('user', None)
        if uid is not None:
            users.pop(uid, None)
        return redirect('/', 307)

    return app

def get_set_tracks(url, collection):

    df, title = getTracks(url)
    track_uris = []

    for row in df.itertuples(index=True, name='Pandas'):
        trackName = getattr(row, 'Song')
        artistName = getattr(row, 'Artist')
        track_artist = trackName + ' ' + artistName
        track, = spotify.search(track_artist,
                                 types=('track',), limit=1)
        collection.insert_one({'Artist' : artistName,
                              'Song' : trackName})
        try:
            track_uris.append(track.items[0].uri)
        except Exception:
            continue

    return track_uris, title


if __name__ == '__main__':
    app = app_factory()
    app.config.from_pyfile('config.py')
    app.run('127.0.0.1', 5000)