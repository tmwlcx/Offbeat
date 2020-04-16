# Offbeatr
>*Class* Offbeatr (random_state=823)

Python class that performs acquisition of song data and uses [MiniBatchKMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.MiniBatchKMeans.html) and [AgglomerativeClustering](https://scikit-learn.org/stable/index.html) from the [Scikit-learn library](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.AgglomerativeClustering.html) to cluster song data by relevant features. All feature information is derived from the [Spotify API](https://developer.spotify.com/).

---

## Parameters:

**random\_state: *int or None, default=823***
>The random initialization of the random number generator. From [numpy.random.RandomState](https://docs.scipy.org/doc/numpy-1.15.0/reference/generated/numpy.random.RandomState.html)

---

## Methods:

**\_\_init\_\_**(*self, random_state*)
>Initialize self.
---


**get\_songs**(*self, songfile=None, host='35.198.88.209', user='teameleven', password='dbpassword', database='SPOTIFY'*)
>Get songs, either from a connection to the database or with a local .csv file containing the required songs data that returns from the spotify API.
>
>#### Parameters:
>
>>**songfile : *Path, default=None***
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;the path to a .csv file containing songs data downloaded from the Spotify API.
>>
>>---
>>
>>**host : *string, default='35.198.88.209'***
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;The hostname or IP address of the database containing spotify API song data. Note that for security reasons, to connect to the default database your own IP address must have been previously whitelisted with the Team 11 Google Cloud account. 
>>
>>---
>>
>>**user : *string, default='teameleven'***
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;The username to connect to the database.
>>
>>---
>>
>>**password : *string, default='dbpassword'***
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;The database user's password.
>>
>>---
>>
>>**database : *string, default='SPOTIFY'***
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;The name of the database.
>>
>>---
>
>
>#### Returns:
>
>>**self**
>>
>>---
>>
>>**qt.pickle**
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;Saves a local file called *'qt.pickle'* that can be used to read in new data using the same transform.
>>
>
>
>#### Attributes:
>
>>**N : *int***
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;The number of songs in the data.
>>
>>---
>>
>>**songs : *pandas.DataFrame, shape(N, p)***
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;A pandas dataframe containing N rows and p attributes read in from the database.
>>
>>---
>>
>>**raw_data : *numpy.ndarray, shape(N,8)***
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;Returns normalized data for each of 8 features. Features are *'danceability'*, *'energy'*, *'loudness'*, *'speechiness'*,*'acousticness'*, *'liveness'*, *'valence'*, *'tempo'*. This data is normalized using the Scikit-learn library's QuantileTransformer power transformer function.
>>
>---


**get\_starting\_clusters**(*self, mb\_kmeans\_n\_clusters=25000, random\_state=0, batch\_size=1000000, verbose=False*)
>Uses mini-batch kmeans from the Scikit-learn library to cluster the songs into initial seed clusters.
>
>#### Parameters:
>
>>**mb\_kmeans\_n\_clusters : *int, default=25000***
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;The number of initial seed clusters to create from the song file. Lower values are less representative of the song data, but provide substantial increase in performance. 
>>
>>---
>>
>>**random\_state : *int, default=0***
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;The random state initialization of the mini batch kmeans engine. 
>>
>>---
>>
>>**batch\_size : *int, default=100000***
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;The batch size for each run of the minibatch kmeans algorithm. Lower values help prevent out-of-memory errors. 
>>
>>---
>>
>>**verbose : *boolean, default=False***
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;Whether to print the status of the mini batch KMeans algorithm as it fits and predicts the data. 
>>
>>---
>
>
>
>#### Returns:
>
>>**self**
>>
>>---
>
>
>
>#### Attributes:
>
>>**mb_kmeans : *sklearn MiniBatchKMeans object***
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;See [sklearn](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.MiniBatchKMeans.html) for more information on this object.
>>
>>---
>>
>>**preds : *numpy.ndarray, shape(num_songs,)***
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;Seed cluster labels for each of the songs as determined by the MiniBatchKMeans algorithm.
>
>---


**agglom\_clusters**(*self, cluster_sizes=[3800,2528,1264,632]*)
>Uses the Agglomerative Clustering algorithm from the Scikit-learn library to perform hierarchical agglomerative clustering.
>
>#### Parameters:
>
>>**cluster\_sizes : *list of ints, default=[3800,2528,1264,632]***
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;A list of integers containing the cluster sizes for each level. The number of levels is derived from the structure of this list. The default values are for 4 levels and were chosen based on the loose number of 1264 genres of music. See [here](https://www.theguardian.com/music/2014/sep/04/-sp-from-charred-death-to-deep-filthstep-the-1264-genres-that-make-modern-music) for more information.
>
>---
>#### Returns:
>
>>**self**
> ---
>
>#### Attributes:
>
>>**songs_labeled_ : *pandas.DataFrame, shape(N, number_levels)***
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;A Pandas DataFrame object containing all N songs in the dataset and their corresponding number_levels of levels. 
>>
>>---
>>
>>**centroids_ : *pandas.DataFrame, shape(sum(cluster_sizes), 8)***
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;A Pandas DataFrame object containing the centroids computed for every label.
>
>---


**export\_csv**(*self, save_songs=True, save_centroids=True, num_parts=20*)
>    Saves the *songs_labeled_* and *centroids_* DataFrame objects as .csv files in the current folder.
>
>#### Parameters:
>
>>**save_songs : *boolean, default=True***
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;Whether to save the *songs_labeled_* DataFrame object. Depending on the value of **num_parts**, this file can be broken down into multiple files for easier transfer.
>>
>>---
>>
>>**save_centroids : *boolean, default=True***
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;Whether to save the *centroids* DataFrame object. 
>>
>>---
>>
>>**num_parts : *int, default=20***
>>
>>    &nbsp;&nbsp;&nbsp;&nbsp;The number of .csv files to break up the *songs_labeled_* DataFrame into.
>---
>
>#### Returns:
>
>>**self**
>
>---
>


**beat\_master**(*\*\*kwargs*)
>    Runs the entire clustering and saving operation. Accepts *\*\*kwargs* from any function in the Offbeatr class.
>
>
>#### Returns:
>
>>**self**
>
>---
>
