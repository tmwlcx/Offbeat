Analytics Update
We are using agglomerative clustering which is a bottom-up form of hierarchical clustering. During our initial attempts, all 11 features were taken as-is (no transformations of the data, and all variables in the clustering model). Based on the groupings of songs that resulted from this raw approach, we felt that more was needed in the way of pre-processing the data. We visualized the song data in 2- and 3-Dimensions using principal component transformation and found a single tight cluster of data. We believe that a combination of approaches will assist us in "pulling apart" the more tightly grouped song data. Our approach to this is two-fold: first we perform feature selection, and second we transform the remaining features.

We removed the following variables on the basis of correlation of variables and ability to transform:
	* key (categorical),
	* mode (boolean), and
	* instramentalness (numeric).
Based on analysis of a smaller dataset, the removal of these features does not adversely impact the clustering. 

We transform the remaining variables to Gaussian distribution, using **Quantile Transformation** or **Power Transformation**. Quantile transformation uses the following formula to place the features into a desired distribution: $$G^{-1}(F(X))$$ where $G^{-1}$ is the quantile function of the desired distribution (here, Gaussian), and $F$ is the CDF of the distribution of the variable $X$. The caveat with using quantile transforms is that it distorts the distance between features. We believe the distortion of distance between features is necessary in order to uncoil the tight grouping of song data as described above. 

Power transformation is another means of taking one distribution and applying transforms to it in order to make it appear like another distribution. Box-Cox and Yeo-Johnson are two popular methods of power transform. We are exploring power transforms as an alternative to quantile transforms. 