**Put links to papers here**

**Reminders:**

* We need three long papers or book chapters per group member (15 total)
* "Long papers" refer to typical papers published at top academic venues (e.g., KDD, CHI, ICML). They are usually at least 8-10 pages long, in 2-column format, which translate into 5000 or more words
* Short papers would be 4-5 pages or fewer, and are not worth full points
* Papers should be peer reviewed
---

>Cilibrasi, R., Vitányi, P., & Wolf, R. d. (2004). Algorithmic Clustering of Music Based on String Compression. Computer Music Journal, 49-67. doi:10.1162/0148926042728449. https://www.mitpressjournals.org/doi/abs/10.1162/0148926042728449?journalCode=comj


>Kim, D., Kim, K.-s., Park, K.-H., & Lee, J.-H. (2007). A music recommendation system with a dynamic k-means clustering algorithm,. Sixth International Conference on Machine Learning and Applications (ICMLA 2007) (pp. 339-4032007). Cincinnati, OH: IEEE. doi:10.1109/ICMLA.2007.97. https://ieeexplore.ieee.org/document/4457263

>Renshaw, E., & Platt, J. (2009, August 4). USA Patent No. 7,571,183 B2. https://patents.google.com/patent/US7571183B2/en

>Tsai, W.-H., & Bao, D.-F. (2010). Clustering Music Recordings Based on Genres. 2010 International Conference on Information Science and Applications (pp. 1-5). Seoul, South Korea: IEEE. doi:10.1109/ICISA.2010.5480365. https://ieeexplore.ieee.org/document/5480365

>Tsai, W.-H., Rodgers, D., & Wang, H.-M. (2004). Blind Clustering of Popular Music Recordings Based on Singer Voice Characteristics. Computer Music Journal, 28(3). doi:10.1162/0148926041790630. https://doi.org/10.1162/0148926041790630

# Technical paper, not peer reviewed
>Kazunori Sato (Google (2012). An Inside Look at Google BigQuery. https://cloud.google.com/files/BigQueryTechnicalWP.pdf

# Found this, references our DBMS text book last year, but was added after the physical print, so I included the link I found it at
Elmasri, R., & Navathe, S. (2016). Fundamentals of database systems (Seventh ed.). https://sceweb.sce.uhcl.edu/helm/DataBaseSystems/References/AppendixD.pdf

# Not Peer reviewed, but very useful so vote?
Müllner, D. (2011). Modern hierarchical, agglomerative clustering algorithms. https://arxiv.org/pdf/1109.2378.pdf

# On recommendation engine algorithms (collaborative filtering and such): 
https://ebookcentral.proquest.com/lib/gatech/reader.action?docID=1884200&query=music+recommendation+engines#

# Useful references, maybe not useable?
https://www.sqlservercentral.com/articles/hierarchies-on-steroids-1-convert-an-adjacency-list-to-nested-sets

Handy little overview of clustering methods
http://www.ijcsit.com/docs/Volume%205/vol5issue06/ijcsit2014050688.pdf

**Whitepaper - AWS Datawarehousing with Redshift**

http://d0.awsstatic.com/whitepapers/enterprise-data-warehousing-on-aws.pdf

* Pros - fast, scalable and accessible datawarehousing.  Useful for analytical purposes and can be queried via SQL like syntax (no need to learn new technology).

* Cons - Does not support data access via API.  This will need to be handled via other tech layers.  Not ideal for quickly serving database to a web application.

* Summary - Useful for pre-storing clusters, but may not be ideal for serving data to our front end quickly for visualization.  This often requires a second database layer (Postgressql) which adds an unneccsary amount of complexity.

**Data stream clustering by divide and conquer approach based on vector model**

Khalilian, M., Mustapha, N. & Sulaiman, N. Data stream clustering by divide and conquer approach based on vector model. Journal of Big Data 3, 1 (2016). https://doi.org/10.1186/s40537-015-0036-x

* Pros - Increased clustering quality and performance as compare to traditional methods.

* Cons - A novel approach to clustering adds complexity to the process.  Also there may not be an existing R or Python package for this, requiring additional custom code to be built.

* Summary - The divide and conquer approach uses a vector model and k-means divide a conquer approach to overcome some of the shortcomings of other data stream clustering solutions.

**Cluster analysis and display of genome-wide expression patterns**

* Pros - Allows for more flexibility than typical clustering methods and lends itsself well to visualization via dendrograms.

* Cons - Can be more difficult to implement on a larger dataset due to higher time complexity of processing the algorithm.  Also, on a larger dataset the dendrograms can become overwhelmingly divided into to many levels.

* Summary - Example of the use of hierarchial expression to cluster various combinations of genetic factors.  This method allowed the researchers to find patterns in the data such as clusters of redundant representations of genes and genes of similar function.

Michael B. Eisen, Paul T. Spellman, Patrick O. Brown, David Botstein Proceedings of the National Academy of Sciences Dec 1998, 95 (25) 14863-14868;

**Principal Components Analysis**

* Pros - helps removes correlated features and reduce the number of dimensions.  This step is key given that this model needs to be visualized and it is hard to visualize with many dimensions.  Also, hierarchical clustering is computationally intensive and will perform better with less features.

* Cons - using principal components instead of features, the data can seem less readable and more difficult to interpret.  

* Summary - A popular and well known approach for deriving a lower number of features from a larger set of attributes.

Data Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani. An Introduction to Statistical Learning : with Applications in R. New York :Springer, 2013. Chapter 10 373-414
**Visualization Stuff**

* Data Visualization with d3.js
https://ebookcentral.proquest.com/lib/gatech/detail.action?docID=1389320

* Data Science for Dummies (when to use d3.js and how to choose your visualization type)
https://ebookcentral.proquest.com/lib/gatech/reader.action?docID=4812516&ppg=7
