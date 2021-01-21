import pandas as pd
import joblib
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC


# load our dataset
df_all=pd.read_csv("data.csv")

X=df_all[["acousticness", "danceability", "liveness","energy", "instrumentalness", "loudness", "speechiness"]] #select features



scaler=preprocessing.MinMaxScaler()


loudness=X["loudness"].values
loudness_scaled=scaler.fit_transform(loudness.reshape(-1, 1))

X["loudness"]=loudness_scaled

features=X.values

model = KMeans(n_clusters=5)
model = model.fit(features)


predictions=model.predict(features) #make predictions

df_all['cluster']=predictions

df_classify=df_all[["acousticness", "danceability", "liveness","energy", "instrumentalness", "loudness", "speechiness","cluster"]]#selecting features


X=df_classify.iloc[:,:-1].values
Y=df_classify.iloc[:,-1].values



X_train, X_test, y_train, y_test=train_test_split(X,Y,test_size=0.2)

X_train[:,5]=scaler.fit_transform(X_train[:,5].reshape(-1, 1)).reshape(-1,)
X_test[:,5]=scaler.transform(X_test[:,5].reshape(-1, 1)).reshape(-1,)

classifier = SVC(kernel ='poly', random_state = 0)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
#prediction = classifier.predict(X_test)



# Save the model to disk
joblib.dump(classifier, 'classifierNew.joblib')














