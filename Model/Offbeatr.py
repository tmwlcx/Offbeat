import pandas as pd
import numpy as np
from sklearn.preprocessing import QuantileTransformer
from sklearn.cluster import MiniBatchKMeans
from sklearn.cluster import AgglomerativeClustering

class Offbeatr(object):
    def __init__(self, path_to_songdata,random_state=823):
        self.rng = np.random.RandomState(random_state)
        self.keepers = ['danceability', 'energy', 'loudness', 
                                  'speechiness','acousticness', 'liveness', 
                                  'valence', 'tempo']
        self.p = len(self.keepers)
        self.qt = QuantileTransformer(output_distribution='normal',random_state=self.rng)
        self.songs = pd.read_csv(path_to_songdata, skiprows=[1])
        self.N = self.songs.shape[0]
        self.info_cols = ['song_id', 'song_name', 'artist_id', 'album_id', 'track_href']
        self.songs_labeled_ = self.songs[['song_id']].copy()
        self.raw_data = self.qt.fit_transform(np.array(self.songs[self.keepers]))

    def get_starting_clusters(self, mb_kmeans_n_clusters=25000, random_state=0, batch_size=100000, verbose=0):
        print('computing starting clusters')
        self.mb_kmeans = MiniBatchKMeans(n_clusters=mb_kmeans_n_clusters, random_state=random_state, batch_size=batch_size, verbose=verbose)
        self.preds = self.mb_kmeans.fit_predict(self.raw_data)
        
        
        
    def agglom_cluster(self, cluster_sizes=[3800,2528,1264,632]):
        """Run the aglomerative clustering algorithm"""
        #inits
        num_levels = len(cluster_sizes)
        centroids = np.zeros((sum(cluster_sizes), self.p))
        fit_list=[]
        colnames = []
        
        #calculate the agglomerative cluster labels
        print('performing agglomerative clustering')
        for i in range(num_levels):
            agglom = AgglomerativeClustering(n_clusters=cluster_sizes[i])
            fit = agglom.fit_predict(self.mb_kmeans.cluster_centers_)
            fit_list.append(fit+sum(cluster_sizes[:i]))

        for i in range(num_levels):
            level_labels = [fit_list[i][self.preds[j]] for j,_ in enumerate(self.preds)]
            colnames.append("level"+str(i))
            self.songs_labeled_[colnames[i]] = level_labels
        print("DataFrame created: 'songs_labeled_'")

        #calculate centroids
        for i in range(num_levels):
            colname = colnames[i]
            val = sum(cluster_sizes[:i])
            for j in range(val,val+cluster_sizes[i]):
                centroids[j,:] = np.mean(self.raw_data[self.songs_labeled_[self.songs_labeled_[colname]==j].index], axis=0)
        self.centroids_ = pd.DataFrame(centroids)
        self.centroids_.columns = self.keepers
        print("DataFrame created: 'centroids_'")
        
    def export_csv(self, save_songs=True, save_centroids=True, num_parts=20):
        if save_songs == True and save_centroids == True:
            print("creating 'songs_labeled_{id}.csv' and 'centroids.csv'")
            for id, df_i in  enumerate(np.array_split(self.songs_labeled_, num_parts)):
                df_i.to_csv('songs_labeled_{id}.csv'.format(id=id), index=False)
            self.centroids_.to_csv('centroids.csv', index=False)
        elif save_songs == True:
            print("creating songs_labeled_{id}.csv")
            for id, df_i in  enumerate(np.array_split(self.songs_labeled_, num_parts)):
                df_i.to_csv('songs_labeled_{id}.csv'.format(id=id), index=False)
        elif save_centroids == True:
            print("Creating 'centroids.csv'")
            self.centroids_.to_csv('centroids.csv', index=False)
        else:
            print('nothing to do')
    
    def beat_master(self, mb_kmeans_n_clusters=25000, random_state=0, batch_size=100000, verbose=0,
                       cluster_sizes=[3800,2528,1264,632], save_songs=True, save_centroids=True, num_parts=20):
        self.get_starting_clusters(mb_kmeans_n_clusters, random_state, batch_size, verbose)
        self.agglom_cluster(cluster_sizes)
        self.export_csv(save_songs, save_centroids, num_parts)
        print('done!')
            
            
off_beat = Offbeatr(path_to_songdata='Partition1.csv')
off_beat.beat_master()