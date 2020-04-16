# Offbeatr

File that performs acquisition of song data and uses [MiniBatchKMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.MiniBatchKMeans.html) and [AgglomerativeClustering](https://scikit-learn.org/stable/index.html) from the [Scikit-learn library](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html) to cluster song data by relevant features. All feature information is derived from the [Spotify API](https://developer.spotify.com/).

---

## Parameters:

>**random_state: *int or None, default=823***
>>The random initialization of the random number generator. From [numpy.random.RandomState](https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.random.RandomState.html)

---

## Methods:

>**\_\_init\_\_**(*self, random_state*)
>>Initialize self.
>---
>get\_songs(*self, songfile=None, host='35.198.88.209', user='teameleven', password='dbpassword', database='SPOTIFY'*)
>>Get songs, either from a connection to the database or with a local .csv file containing the required songs data that returns from the spotify API.
>>
>>### Parameters:
>>
>>**songfile : *Path, default=None***
>>    the path to a .csv file containing songs data downloaded from the spotify api
>>
>>**host : *string***
>>    The hostname or IP address of the database containing spotify API song data. Note that for security reasons, to connect to the default database your own IP address must have been previously whitelisted with the Team 11 Google Cloud account. 
>>
>>**user : *string***
>>    The username to connect to the database
>>
>>**password : *string***
>>    The database user's password
>>
>>**database : *string***
>>    The name of the database
>>
>>---
>**get\_starting\_clusters**(*self, mb_kmeans_n_clusters=25000, random_state=0, batch_size=1000000, verbose=False*)
