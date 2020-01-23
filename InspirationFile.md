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

Project Idea: <b>Musical Map</b>

[Video on this concept](https://youtu.be/uIKSIf9p2ZI) (skip to 6:47 to hear him explain what I'm talking about)

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

***********************************************************

Name: Jeff

Project Idea: <b>Political Canvassing Map</b>

_Political canvassing_ is the systematic initiation of direct contact with individuals in order to deliver a political message and encourage actions such as voting.  For many elections, this is done by knocking on doors and talking to individuals directly.  Many political campaigns have limited resources and as a result need to efficiently reach voters that are most likely to support their candidate.  Using pubically available voter data, a map can be constructed to show the largest clusters of receptive voters.  A campaign now has a roadmap of areas to canvas where they expect to get the most engagement and make the best use of their resources.

I would envision this tool being used for a relatively small geographic area, such as a town or small city.  For a large city like NYC, this would probably only work for a single borough or even a portion of a borough.  For too large of an area, the usage of this tool would be impractical.

Additionally, this system could be fine tuned to provide a specialized roadmap based on demographic information.  For instance, specific clusters could be generated based on voters that are over 60 years old as part of a specific canvassing effort to highlight that a specific candidate is supportive of Social Security.  This could also be further refined to use some type of shortest path algorithm to instruct the end users the most efficient way to cover territory within a given cluster.

Here is an example of the data available:
[https://www.pavoterservices.pa.gov/Pages/PurchasePAFULLVoterExport.aspx]
Fields available:
voter ID number, name, sex, date of birth, date registered, status (i.e., active or inactive), date status last changed, party, residential address, mailing address, polling place, date last voted, all districts in which the voter votes (i.e., congressional, legislative, school district, etc.), voter history, and date the voter’s record was last changed.

Project Requirements:
1. Big Data - there are millions of registered voters so plenty of data to draw from.
2. Analytics Models - K means clustering and shortest path algorithms could potentially be used
3. Interactive front end - Provide a map that can be tweaked based on certain demographics markers (under 35, over 60, income level, etc).  Click on a cluster to zoom in and provide naviagtion instructions.


<u>Pros</u>:
* Lot's of data to work with - counties typically provide a downloadable csv file of voter registration data.
* Easy to visualize - the data comes with addresses so we can easily create our own maps
* It is an election year, so this is a topic that is on people's minds

<u>Cons</u>:
* In practice, the shortest path algorithm could be messy.  It might be hard to account for one way streets, traffic, etc
* Clustering algorithm might not provide a ton of new value.  What if it just points you to the most populous areas?
***********************************************************

Name: Drew

Project Idea: <b>Twitter Election Results</b>

I'm personally really interested in applying NLP techniques to understand sentiment and track patterns. I think it would be an interesting challenge to gather tons of Twitter data from around the US (maybe state by state) to see if any factors in the data are predictive of election results. For example: does Twitter sentiment & content in a given area predict election results at all? And can historical data be normalized against current data to provide insight into the next election cycle?

Given that Twitter never stops generating data, we could potentially explore building a front end that continues to update with new data regularly; it wouldn't have to simply query a static DB that we built somewhere.

Project Requirements:
1. Big Data - check
2. Analytics Models - NLP, regression, time series
3. Interactive front end - lots of directions that we could go with it! map-based is a logical choice; could potentially work personalization into this as well to let the user see data relevant to their location; could also go with the real-time aspect to provide a very interesting & interactive UI

<u>Pros</u>:
* Certainly meets the "big data" requirement
* Potential to be incredibly impactful depending on what we find
* Lots of directions that we could go with it!

<u>Cons</u>:
* Lots of directions that we could go with it!
* Has probably been researched a ton already ... so we may not actually do anything new or interest anyone with this

***********************************************************
