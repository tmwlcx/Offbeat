Add your Name, List and explain your idea for a project:


Tyler Inness : The Complicated Thing
  Will write about it later

***********************************************************
Name: Tim

Project Idea: <b>Dream Home</b>

The user inputs features of their dream home: 
* Property Type: Single Family House, Townhome, Flat, etc.
* No. bedrooms
*	No. bathrooms
*	Other features: e.g., pool, attached garage, large lot, in-home planetarium, etc.

The user also inputs their desired location and a price ceiling

A clustering algorithm is used to identify properties that match the user’s dream home and are sorted in that order. Depending on how fancy we wanted to get, the application could also compare the suggested dream home against previously sold properties to give the customer more information regarding the current market, etc.


<u>Pros</u>: 
*	relatively simple project 
*	possibility to add lots of features as we think of them

<u>Cons</u>: 
* Scraping MLS data might be a challenge:
*	Scraping Zillow data is against that website’s terms of use, we could use other data sources (such as Melbourne housing dataset from Kaggle), but we might be limited to a static dataset.
*	The differentiator between what websites like Zillow already provide would be the clustering algorithm -- (so it would need to be good)

***********************************************************
Name: Waverly

Projece Idea: <b>Musical Map</b>

Spotify "Wrapped 2019" was a big deal in 2019 as people were able to see and share metrics on their music listening patterns over the past year and decade (my instagram was saturated with people sharing their top 10 artists, songs and albums). I think people got excited when they saw a visually stunning tool tell a personal story about them using their own data.

In that vein, I think we could build a tool that highlights music that is really _different_ from what you typically listen to. <b>I think people would be intrigued by an interactive tool that tells them a story about what music they might be missing out on!</b> There are _so_ many recommendation engines that push music at you that all starts to sound the same... Our tool would help people discover new sounds/artists/genres that they might otherwise never find.

We could do clustering given a user's spotify creds (so we would see their listening history and playlists), and we could make an interactive viz. I'm picturing some sort of relational map where we highlight clusters that are far away from the music that the user typically listens to.

<u>Pros</u>:
* I think people would find this product interesting and fun! People dig this kind of personalized self-discovery tool ([article for proof](https://www.theatlantic.com/technology/archive/2018/12/spotify-wrapped-and-data-collection/577930/))
* The Spotify api is allegedly cool and easy to work with, and has some pretty detailed info. For example, you can get down to detail like the tempo, rythym, presence of spoken words, etc... for any track
* There's a ton of data at our disposal with Spotify's api alone

<u>Cons</u>:
* This idea is still pretty open ended. We could structure this a few different ways, which means more discussion/work on defining the problem/product
* I can't tell if this is a tool that only I would want to use... maybe most people _don't_ want to discover music that is super different from what they already listen to!
