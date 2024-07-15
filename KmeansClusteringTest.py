import numpy as np
import pandas as ph
import plotly.graph_object as go


from sklearn.cluster import KMeans

def random_centroids(values, criterion): #criterion <- 군집 개수
    centroids = []
    
    for i in range(criterion):
        centroids = values[rand.randint(0, len(values) - 1)]
        centroids.append(centroid)