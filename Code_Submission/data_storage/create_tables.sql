CREATE TABLE `songs` (
  `song_id` char(22) NOT NULL,
  `song_name` varchar(500) DEFAULT NULL,
  `artist_id` char(22) DEFAULT NULL,
  `album_id` char(22) DEFAULT NULL,
  `track_href` char(56) DEFAULT NULL,
  `duration_ms` int(11) DEFAULT NULL,
  `time_signature` int(11) DEFAULT NULL,
  `danceability` decimal(12,8) DEFAULT NULL,
  `energy` decimal(12,8) DEFAULT NULL,
  `musical_key` int(11) DEFAULT NULL,
  `loudness` decimal(12,8) DEFAULT NULL,
  `mode` int(11) DEFAULT NULL,
  `speechiness` decimal(12,8) DEFAULT NULL,
  `acousticness` decimal(12,8) DEFAULT NULL,
  `instrumentalness` decimal(12,8) DEFAULT NULL,
  `liveness` decimal(12,8) DEFAULT NULL,
  `valence` decimal(12,8) DEFAULT NULL,
  `tempo` decimal(12,8) DEFAULT NULL,
  PRIMARY KEY (`song_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `songs_labeled` (
  `song_id` char(22) NOT NULL,
  `level0` int(11) DEFAULT NULL,
  `level1` int(11) DEFAULT NULL,
  `level2` int(11) DEFAULT NULL,
  `level3` int(11) DEFAULT NULL,
  PRIMARY KEY (`song_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `centroids` (
  `centroid_id` int(11) NOT NULL,
  `danceability` decimal(12,8) DEFAULT NULL,
  `energy` decimal(12,8) DEFAULT NULL,
  `loudness` decimal(12,8) DEFAULT NULL,
  `speechiness` decimal(12,8) DEFAULT NULL,
  `acousticness` decimal(12,8) DEFAULT NULL,
  `liveness` decimal(12,8) DEFAULT NULL,
  `valence` decimal(12,8) DEFAULT NULL,
  `tempo` decimal(12,8) DEFAULT NULL,
  PRIMARY KEY (`centroid_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `albums` (
  `album_id` char(22) NOT NULL,
  `artist_id` char(22) DEFAULT NULL,
  `album_name` varchar(500) DEFAULT NULL,
  `album_uri` char(37) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `artist` (
  `artist_id` char(22) NOT NULL,
  `artist_name` varchar(250) DEFAULT NULL,
  `artist_uri` char(37) DEFAULT NULL,
  `followers` int(11) DEFAULT NULL,
  PRIMARY KEY (`artist_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
