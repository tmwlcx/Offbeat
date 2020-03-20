#	Data Gathering and Data Storage (Completed)
1.	Data mapping of features provided by Spotify
a.	Pulled a sample of 10,000 songs to determine appropriate data types to store features in the database (string length, number of decimals, etc)
2.	Creation of relational schema in a cloud based MYSQL instance
a.	Object types include songs, artists, and albums
b.	Cloud storage enables automated backups and easy activity from cloud servers
3.	Scalable API calls to the multiple Spotify endpoints
a.	Cloud servers allow for simple multi-threading.    
# Connectivity (In progress)
1.	Enabling of public static IP access between MYSQL and web server
a.	This will allow for custom data to be sent to the front end based on the user’s top songs.
2.	Spotify User Authorization
a.	Will be used to pull a sample of user’s top songs for analysis
