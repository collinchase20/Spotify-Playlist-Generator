import pandas as pd
from sklearn import preprocessing
from spotifyRequests import spotify
import joblib


class GeneratePlaylists():

    def __init__(self):
        self.classifier = joblib.load("classifier.joblib")
        self.scaler = preprocessing.MinMaxScaler()
        self.currentPlaylistUris = []
        self.currentPlaylistNames = []
        self.userSavedSongs = []
        self.userSavedAudioFeatures = []
        self.leastPopularTracks = []
        self.notVeryPopularTracks = []
        self.averagePopularityTracks = []
        self.prettyPopularTracks = []
        self.mostPopularTracks = []
        self.rapTracks = []
        self.energeticTracks = []
        self.calmTracks = []
        self.thinkingTracks = []
        self.chillTracks = []
        self.uridict = {}
        self.popularityDict = {}
        self.likedIds = []
        self.likedUris = []



    def moodPlaylists(self, auth_header):
        if len(self.userSavedSongs) == 0:
            GeneratePlaylists.getUserSavedSongs(self, auth_header)
        if len(self.userSavedAudioFeatures) == 0:
            GeneratePlaylists.initializeMoodData(self, auth_header)
        df = GeneratePlaylists.setUpDataFrame(self)
        GeneratePlaylists.scale_features(self, self.scaler, df)
        features = GeneratePlaylists.get_features(self, df)
        GeneratePlaylists.make_predictions(self, features, df)
        GeneratePlaylists.make_sorted_songs(self, df)
        GeneratePlaylists.sortedSongsToTracks(self, self.currentPlaylistUris)
        GeneratePlaylists.setCurrentPlaylistsNames(self, "mood")




    def popularityPlaylists(self, auth_header):
        if len(self.userSavedSongs) == 0:
            GeneratePlaylists.getUserSavedSongs(self, auth_header)
        GeneratePlaylists.initializePopularityData(self)
        GeneratePlaylists.setCurrentPlaylistsNames(self, "popularity")





    def setCurrentPlaylistsNames(self, name):
        if name == "mood":
            self.currentPlaylistNames = ['Rap', 'Energetic/Dancing', 'Calm/Romantic', 'Studying/Thinking', 'Chill']
        elif name == "popularity":
            self.currentPlaylistNames = ['Least Popular', 'Not Very Popular', 'Average Popularity', "Pretty Popular",
                                          "Most Popular"]
        else:
            raise Exception("Error occured while setting the current playlists names")





    def getUserSavedSongs(self, auth_header):
        off = 0
        while True:
            content = spotify.get_users_saved_tracks(auth_header, off)
            self.userSavedSongs += content['items']
            if content['next'] is not None:
                off+= 50
            else:
                break





    def initializePopularityData(self):
        leastPopularUri = []
        notVeryPopularUri = []
        averagePopularityUri = []
        prettyPopularUri = []
        mostPopularUri = []
        for i in self.userSavedSongs:
            theTrack = i['track']
            popularity = i['track']['popularity']
            theUri = i['track']['uri']
            self.uridict[i['track']['uri']] = i['track']
            if popularity <= 20:
                leastPopularUri.append(theUri)
                self.leastPopularTracks.append(theTrack)
            elif popularity > 20 and popularity <= 40:
                notVeryPopularUri.append(theUri)
                self.notVeryPopularTracks.append(theTrack)
            elif popularity > 40 and popularity <= 60:
                averagePopularityUri.append(theUri)
                self.averagePopularityTracks.append(theTrack)
            elif popularity > 60 and popularity <= 80:
                prettyPopularUri.append(theUri)
                self.prettyPopularTracks.append(theTrack)
            elif popularity > 80 and popularity <= 100:
                mostPopularUri.append(theUri)
                self.mostPopularTracks.append(theTrack)

        self.currentPlaylistUris.append(leastPopularUri)
        self.currentPlaylistUris.append(notVeryPopularUri)
        self.currentPlaylistUris.append(averagePopularityUri)
        self.currentPlaylistUris.append(prettyPopularUri)
        self.currentPlaylistUris.append(mostPopularUri)







    def initializeMoodData(self, auth_header):
        names = []
        ids = []
        uris = []

        for i in self.userSavedSongs:
            names.append(i['track']['name'])
            ids.append(i['track']['id'])
            uris.append(i['track']['uri'])
            self.uridict[i['track']['uri']] = i['track']

        self.likedIds = ids
        self.likedUris = uris
        index = 0
        audio_features = []
        accum = 0

        while index < len(ids):
            param = ""
            for i in range(100):
                if accum != len(ids):
                    param += ids[accum]
                    accum += 1
                    if i != 99:
                        param += ","
            feat = spotify.get_songs_audio_features(auth_header, param)
            audio_features += feat["audio_features"]
            index += 100

        self.userSavedAudioFeatures = audio_features






    def setUpDataFrame(self):
        features_list = []
        for features in self.userSavedAudioFeatures:
            try:
                features_list.append([features['acousticness'], features['danceability'],
                                      features['liveness'], features['energy'],
                                      features['instrumentalness'], features['loudness'],
                                      features['speechiness']])
            except:
                raise Exception(self.userSavedAudioFeatures)

        mydf = pd.DataFrame(features_list,
                            columns=["acousticness", "danceability", "liveness", "energy", "instrumentalness",
                                     "loudness",
                                     "speechiness"], index=self.likedUris)

        return mydf






    def scale_features(self, scaler, df):
        loudness = df['loudness'].values
        loudness_scaled = scaler.fit_transform(loudness.reshape(-1, 1))
        df['loudness'] = loudness_scaled




    def get_features(self, df):
        features = df.values
        return features




    def make_predictions(self, features, df):
        predictions = self.classifier.predict(features)
        df['cluster'] = predictions




    def make_sorted_songs(self, df):
        clustered_songs = list(zip(df.index, df.iloc[:, -1]))
        sorted_songs = [[], [], [], [], []]
        for i in range(len(clustered_songs)):
            sorted_songs[clustered_songs[i][1]].append(clustered_songs[i][0])

        #raise Exception(len(sorted_songs[0]), len(sorted_songs[1]), len(sorted_songs[2]), len(sorted_songs[3]), len(sorted_songs[4]))
        #return sorted_songs
        self.currentPlaylistUris = sorted_songs




    def sortedSongsToTracks(self, sorted):
        for i in range(5):
            for j in sorted[i]:
                if i == 0:
                    self.rapTracks.append(self.uridict[j])
                elif i == 1:
                    self.energeticTracks.append(self.uridict[j])
                elif i == 2:
                    self.calmTracks.append(self.uridict[j])
                elif i == 3:
                    self.thinkingTracks.append(self.uridict[j])
                elif i == 4:
                    self.chillTracks.append(self.uridict[j])




    def makeMoodPlaylists(self, sorted_songs, profile, auth):
        for i in range(5):
            playlist_created = spotify.make_playlist(auth, self.moods[i], profile["id"])
            numberOfSongs = len(sorted_songs[i])
            remainder = numberOfSongs % 100
            iterations = numberOfSongs // 100
            if remainder != 0:
                iterations += 1
            fromIndex = 0
            toIndex = 100
            accum = 0
            for j in range(iterations):
                spotify.add_tracks_to_playlist(auth, playlist_created['id'], sorted_songs[i][fromIndex:toIndex])
                fromIndex += 100
                toIndex += 100
                accum += 1





    def createPlaylist(self, profile, auth, playlist, name):
        playlist_created = spotify.make_playlist(auth, name, profile["id"])
        numberOfSongs = len(playlist)
        remainder = numberOfSongs % 100
        iterations = numberOfSongs // 100
        if remainder != 0:
            iterations += 1
        fromIndex = 0
        toIndex = 100
        accum = 0
        for j in range(iterations):
            spotify.add_tracks_to_playlist(auth, playlist_created['id'], playlist[fromIndex:toIndex])
            fromIndex += 100
            toIndex += 100
            accum += 1