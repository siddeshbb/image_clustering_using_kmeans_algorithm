#from pylab import plot,show
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq,whiten

# data generation
data = [[255, 255,], [214, 222,], [214, 1222,], [122, 123,]]
data = array(data)
#data = whiten(data)
print data
#print data
#print data
# computing K-Means with K = 2 (2 clusters)
centroids,_ = kmeans(data,2)
print centroids
'''# assign each sample to a cluster
#idx,_ = vq(data,centroids)

# some plotting using numpy's logical indexing
plot(data[idx==0,0],data[idx==0,1],'ob',
     data[idx==1,0],data[idx==1,1],'or')
plot(centroids[:,0],centroids[:,1],'sg',markersize=8)
show()

'''
