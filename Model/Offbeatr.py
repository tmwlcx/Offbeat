import pandas as pd
import numpy as np
from sklearn.preprocessing import QuantileTransformer
from sklearn.cluster import MiniBatchKMeans, AgglomerativeClustering
import pickle
from joblib import dump


class Offbeatr(object):
    def __init__(self, random_state=823):
        self.rng = np.random.RandomState(random_state)
        self.keepers = ['danceability', 'energy', 'loudness', 'speechiness','acousticness', \
                        'liveness', 'valence', 'tempo']
        
    def get_songs(self, songfile=None, host='35.196.88.209', user='teameleven', 
                  password='dbpassword', database='SPOTIFY'):
        
        """As a security measure, IP must be whitelisted in Google cloud prior to 
        getting song data"""
        if not songfile:
            conn = pymysql.connect(host='35.196.88.209', user='teameleven', \
                                   password='dbpassword', database='SPOTIFY')
            query = """
                    SELECT * 
                    FROM songs
                    """
            print('fetching songs from database')
            self.songs=pd.read_sql(query, conn)
            conn.close()
        else:
            print('reading songs from local file')
            self.songs = pd.read_csv(songfile, skiprows=[1])
        self.N = self.songs.shape[0]
        self.songs_labeled_ = self.songs[['song_id']].copy()
        qt = QuantileTransformer(output_distribution='normal',random_state=self.rng)
        self.raw_data = qt.fit_transform(np.array(self.songs[self.keepers]))
        dump(qt, 'qt.pickle')
        print("Saved transformer to file: 'qt.pickle'")


    def get_starting_clusters(self, mb_kmeans_n_clusters=25000, random_state=0, 
                              batch_size=100000, verbose=0):
        print('computing starting clusters')
        self.mb_kmeans = MiniBatchKMeans(n_clusters=mb_kmeans_n_clusters, \
                                         random_state=random_state, batch_size=batch_size, \
                                         verbose=verbose)
        self.preds = self.mb_kmeans.fit_predict(self.raw_data)
        
    def agglom_cluster(self, cluster_sizes=[3800,2528,1264,632]):
        """Run the aglomerative clustering algorithm"""
        #inits
        num_levels = len(cluster_sizes)
        centroids = np.zeros((sum(cluster_sizes), len(self.keepers)))
        fit_list=[]
        colnames = []
        
        #calculate the agglomerative cluster labels
        print('performing agglomerative clustering')
        for i in range(num_levels):
            agglom = AgglomerativeClustering(n_clusters=cluster_sizes[i])
            fit = agglom.fit_predict(self.mb_kmeans.cluster_centers_)
            fit_list.append(fit+sum(cluster_sizes[:i]))
            level_labels = [fit_list[i][self.preds[j]] for j,_ in enumerate(self.preds)]
            colnames.append("level"+str(i))
            self.songs_labeled_[colnames[i]] = level_labels
        print("DataFrame created: 'songs_labeled_'")

        #calculate centroids
        for i in range(num_levels):
            colname = colnames[i]
            val = sum(cluster_sizes[:i])
            for j in range(val,val+cluster_sizes[i]):
                centroids[j,:] = np.mean(self.raw_data[self.songs_labeled_[ \
                    self.songs_labeled_[colname]==j].index], axis=0)
        self.centroids_ = pd.DataFrame(centroids)
        self.centroids_.columns = self.keepers
        print("DataFrame created: 'centroids_'")
        
    def export_csv(self, save_songs=True, save_centroids=True, num_parts=20):
        #save transformer object as pickle
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
    
    def beat_master(self, songfile=None, host='35.196.88.209', user='teameleven', password='dbpassword', \
                    database='SPOTIFY',mb_kmeans_n_clusters=25000, random_state=0, \
                    batch_size=100000, verbose=0, cluster_sizes=[3800,2528,1264,632], \
                    save_songs=True, save_centroids=True, num_parts=20):
        "This self contained script takes ~2.5 hours to run"
        self.get_songs(songfile, host, user, password, database)
        self.get_starting_clusters(mb_kmeans_n_clusters, random_state, batch_size, verbose)
        self.agglom_cluster(cluster_sizes)
        self.export_csv(save_songs, save_centroids, num_parts)
        print('done!')

# run it        
off_beat = Offbeatr()
off_beat.beat_master()
            
            
            

        
        
        
        
        
