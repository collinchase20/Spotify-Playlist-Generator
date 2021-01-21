from flask import Flask, current_app, request, redirect, render_template, session
from backend import GeneratePlaylists
from spotifyRequests import spotify

app = Flask(__name__)
app.secret_key = 'some secret key'
app.config['MY_OBJECT'] = GeneratePlaylists.GeneratePlaylists()




@app.route("/auth")
def auth():
    return redirect(spotify.AUTH_URL)


@app.route("/callback/")
def callback():

    auth_token = request.args['code']
    auth_header = spotify.authorize(auth_token)
    session['auth_header'] = auth_header
    current_app.config['MY_OBJECT'] = GeneratePlaylists.GeneratePlaylists()
    return profile()


#Check if we recieved a valid access token
def valid_token(resp):
    return resp is not None and not 'error' in resp




@app.route("/")
def index():
    current_app.config['MY_OBJECT'] = GeneratePlaylists.GeneratePlaylists()
    return render_template('profile.html')



@app.route('/profile')
def profile():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        #get profile data
        profile_data = spotify.get_users_profile(auth_header)

        #get user playlist data
        playlist_data = spotify.get_users_playlists(auth_header)

        #get user top artists
        artists = spotify.get_users_top(auth_header, "artists")

        #get user top tracks
        tracks = spotify.get_users_top(auth_header, "tracks")
        
        if valid_token(profile_data):
            return render_template("profile.html",
                               user=profile_data,
                               playlists=playlist_data['items'],
                               top_artists = artists["items"],
                               top_tracks = tracks["items"])

    return render_template('profile.html')




@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/generate')
def generate():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        # get profile data
        profile_data = spotify.get_users_profile(auth_header)

        if valid_token(profile_data):
            return render_template("generate.html",
                                   user = profile_data)

    return render_template("generate.html")




@app.route('/moods_button', methods=['GET', 'POST'])
def moods_button():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        # get profile data
        profile_data = spotify.get_users_profile(auth_header)

        if valid_token(profile_data):
            current_app.config['MY_OBJECT'].moodPlaylists(auth_header)
            rap = current_app.config['MY_OBJECT'].rapTracks
            energetic = current_app.config['MY_OBJECT'].energeticTracks
            calm = current_app.config['MY_OBJECT'].calmTracks
            thinking = current_app.config['MY_OBJECT'].thinkingTracks
            chill = current_app.config['MY_OBJECT'].chillTracks
            return render_template("addPlaylists.html",
                                   user=profile_data,
                                   playlist1 = rap,
                                   playlist2 = energetic,
                                   playlist3 = calm,
                                   playlist4 = thinking,
                                   playlist5 = chill,
                                   header1="Rap",
                                   header2="Energetic/Dancing",
                                   header3="Romantic/Calm",
                                   header4="Studying/Thinking",
                                   header5="Chill")

    return render_template("errorGenerating.html")





@app.route('/popularity_button', methods=['GET', 'POST'])
def popularity_button():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        # get profile data
        profile_data = spotify.get_users_profile(auth_header)

        if valid_token(profile_data):
            current_app.config['MY_OBJECT'].popularityPlaylists(auth_header)
            leastPop = current_app.config['MY_OBJECT'].leastPopularTracks
            notPop = current_app.config['MY_OBJECT'].notVeryPopularTracks
            averagePop = current_app.config['MY_OBJECT'].averagePopularityTracks
            prettyPop = current_app.config['MY_OBJECT'].prettyPopularTracks
            mostPop = current_app.config['MY_OBJECT'].mostPopularTracks
            return render_template("addPlaylists.html",
                                   user=profile_data,
                                   playlist1 = leastPop,
                                   playlist2 = notPop,
                                   playlist3 = averagePop,
                                   playlist4 = prettyPop,
                                   playlist5 = mostPop,
                                   header1 = "Your Deep Cuts (Least Popular)",
                                   header2 = "Not Popular Songs (2nd Least Popular)",
                                   header3 = "Average Popularity",
                                   header4 = "Popular Songs (2nd Most Popular)",
                                   header5 = "Classics (Most Popular)")

    return render_template('errorGenerating.html')





@app.route('/addTracksButton1', methods=['GET', 'POST'])
def addTracksButton1():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        # get profile data
        profile_data = spotify.get_users_profile(auth_header)

        return current_app.config['MY_OBJECT'].createPlaylist(profile_data, auth_header,
                                                              current_app.config['MY_OBJECT'].currentPlaylistUris[0],
                                                              current_app.config['MY_OBJECT'].currentPlaylistNames[0])

    return render_template('errorAdding.html')





@app.route('/addTracksButton2', methods=['GET', 'POST'])
def addTracksButton2():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        # get profile data
        profile_data = spotify.get_users_profile(auth_header)

        return current_app.config['MY_OBJECT'].createPlaylist(profile_data, auth_header,
                                                              current_app.config['MY_OBJECT'].currentPlaylistUris[1],
                                                              current_app.config['MY_OBJECT'].currentPlaylistNames[1])

    return render_template('errorAdding.html')





@app.route('/addTracksButton3', methods=['GET', 'POST'])
def addTracksButton3():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        # get profile data
        profile_data = spotify.get_users_profile(auth_header)

        return current_app.config['MY_OBJECT'].createPlaylist(profile_data, auth_header,
                                                              current_app.config['MY_OBJECT'].currentPlaylistUris[2],
                                                              current_app.config['MY_OBJECT'].currentPlaylistNames[2])

    return render_template('errorAdding.html')





@app.route('/addTracksButton4', methods=['GET', 'POST'])
def addTracksButton4():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        # get profile data
        profile_data = spotify.get_users_profile(auth_header)

        return current_app.config['MY_OBJECT'].createPlaylist(profile_data, auth_header,
                                                              current_app.config['MY_OBJECT'].currentPlaylistUris[3],
                                                              current_app.config['MY_OBJECT'].currentPlaylistNames[3])

    return render_template('errorAdding.html')





@app.route('/addTracksButton5', methods=['GET', 'POST'])
def addTracksButton5():
    if 'auth_header' in session:
        auth_header = session['auth_header']

        # get profile data
        profile_data = spotify.get_users_profile(auth_header)

        return current_app.config['MY_OBJECT'].createPlaylist(profile_data, auth_header,
                                                              current_app.config['MY_OBJECT'].currentPlaylistUris[4],
                                                              current_app.config['MY_OBJECT'].currentPlaylistNames[4])

    return render_template('errorAdding.html')




if __name__ == "__main__":
    app.run(host="0.0.0.0")
