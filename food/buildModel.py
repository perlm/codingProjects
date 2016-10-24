import numpy as np
import math
import  scipy.stats as stats
from sklearn import decomposition, preprocessing, cluster, metrics, cross_validation, svm, feature_selection
from subprocess import Popen

def heirarchical(X,names,k):
	model = cluster.AgglomerativeClustering(n_clusters=k, linkage='ward')
        clusterLabels = model.fit_predict(X)
	silhouette_avg = metrics.silhouette_score(X, clusterLabels)
	print "Clusters=", k, " avg silhouette score:", silhouette_avg
	sample_silhouette_values = metrics.silhouette_samples(X, clusterLabels)

	points = names.size
        clusterLabels = np.reshape(clusterLabels, (points,1))
        sample_silhouette_values = np.reshape(sample_silhouette_values, (points,1))

	forOutput = np.hstack((names,clusterLabels))
	forOutput2 = np.hstack((forOutput,sample_silhouette_values))

        f1 = open('data/heir_%s.data' % (k),'w')
        np.savetxt(f1, forOutput2, delimiter=' ', fmt=('%s','%s','%s'))
        f1.close()
	Popen('sort -nk 2 -nk 3 data/heir_%s.data > data/heir_%s_sort.data' % (k,k), shell = True).wait()

def kmean(X,names,k,write=False):
        model = cluster.KMeans(n_clusters=k) 
        clusterLabels = model.fit_predict(X)
	silhouette_avg = metrics.silhouette_score(X, clusterLabels)
	print "Clusters=", k, " avg silhouette score:", silhouette_avg
	sample_silhouette_values = metrics.silhouette_samples(X, clusterLabels)

	points = names.size
        clusterLabels = np.reshape(clusterLabels, (points,1))
        sample_silhouette_values = np.reshape(sample_silhouette_values, (points,1))

	forOutput = np.hstack((names,clusterLabels))
	forOutput2 = np.hstack((forOutput,sample_silhouette_values))
	forOutput3 = np.hstack((forOutput2,X))

	if write:
	        f1 = open('data/kmean_sub_%s.data' % (k),'w')
	        np.savetxt(f1, forOutput3, delimiter=' ', fmt=(['%s',]*9))
	        f1.close()
		Popen('sort -nk 2 -nk 3 data/kmean_sub_%s.data > data/kmean_sub_%s_sort.data' % (k,k), shell = True).wait()
		Popen('rm data/kmean_sub_%s.data' % (k), shell = True).wait()

def factorAnalysis(X,d,names):
	fa = decomposition.FactorAnalysis(n_components=d)
	fa.fit(X)
	X= fa.transform(X)
	n = np.hstack((names,X))

	print d, np.mean(cross_validation.cross_val_score(fa, X)), "=FA score"

	if d==10:
        	f1 = open('data/fa_out_%s.data' % d,'w')
        	np.savetxt(f1, n, delimiter=' ', fmt=(['%s',]*(d+1)))
        	f1.close()

def pca(X,d,names):
	pca = decomposition.PCA(n_components=d)
	pca.fit(X)
	X= pca.transform(X)
	n = np.hstack((names,X))
	print d, np.sum(pca.explained_variance_ratio_), "=PCA explained variance"

	if d==25:
		f1 = open('data/pca_out_%s.data' % d,'w')
		np.savetxt(f1, n, delimiter=' ', fmt=(['%s',]*(d+1)))
		f1.close()

	return X

def outlierSVM_explore(X,names):
	#use One Class SVM to detect outliers- does not assume gaussian distribution
	n = 0.1
	while n <= 0.9: 
		classifier = svm.OneClassSVM(nu=n, gamma=0)
		classifier.fit(X)
		#y_pred = classifier.decision_function(X)
		y_pred = classifier.predict(X)
        	y_pred = np.reshape(y_pred, (8618,1))

		out = np.where(y_pred==-1)[0].size
		print "OSVM identifies ", out, " as outliers for n=", n
		
        	f1 = open('data/OSVM_%s.data' % n,'w')
		p = np.hstack((names,y_pred))
        	np.savetxt(f1, p, delimiter=' ', fmt=('%s', '%s'))
        	f1.close()

		n += 0.1

def outlierSVM(X,names, n):
	#use One Class SVM to detect outliers- does not assume gaussian distribution
	classifier = svm.OneClassSVM(nu=n, gamma=0)
	classifier.fit(X)
	#y_pred = classifier.decision_function(X)
	y_pred = classifier.predict(X)
       	y_pred = np.reshape(y_pred, (8618,1))

	ind = np.where(y_pred==1)
	X_trimmed = X[ind[0],:]
	names_trimmed = names[ind[0]]

	return X_trimmed, names_trimmed

def processData():
	names = np.genfromtxt('data/foodFacts.data', delimiter=' ', skip_header=1, usecols=0, dtype=str)
        names = np.reshape(names, (8618,1))
	data = np.genfromtxt('data/foodFacts.data', delimiter=' ', skip_header=1)
	#There is no Y! untrained untrained untrained!!!
	X =  data[:,1:]

	#First - Impute: if individual fat missing = 0. total fat missing, replace with sum...
        inds = np.where(np.isnan(X[:,20]))
	X[inds,20] = 0
        inds = np.where(np.isnan(X[:,24]))
	X[inds,24] = 0
        inds = np.where(np.isnan(X[:,25]))
	X[inds,25] = 0
        inds = np.where(np.isnan(X[:,26]))
	X[inds,26] = X[inds,20] + X[inds,24] + X[inds,25]

	# for others... replace nan's with column mean. Naive imputation!
        #col_mean = stats.nanmean(X,axis=0)
        #inds = np.where(np.isnan(X))
        #X[inds]=np.take(col_mean,inds[1])
	#replace nan's with zero
	X = np.nan_to_num(X)

	# Optional: feature selection based on variance. Threshold is arbitrary...
	#X_new = feature_selection.VarianceThreshold(threshold=0.1).fit_transform(X)

	# Alternative: select features based on what i feel like.
	cols = np.array([0, 2, 5, 6, 7, 11, 12, 15, 25 ])
	X = X[:,cols]
	
	#Second - standardize the dataset! mean=0, var=1...
	X = preprocessing.scale(X)

        f1 = open('data/cleaned.data','w')
        np.savetxt(f1, X, delimiter=' ', fmt='%1.3f')
        f1.close()

	return X, names

if __name__ == '__main__':

	#load, standardize, impute
	X, names = processData()

	#remove outliers
	#outlierSVM_explore(X,names)
	X, names = outlierSVM(X,names,0.1)

	#dimensionality reduction
	#for d in xrange(2,10):pca(X,d, names)
	#for d in xrange(2,11):factorAnalysis(X,d, names)
	X= pca(X,6, names)

	#cluster
	#for k in xrange(2,21):kmean(X,names,k)
	kmean(X,names,5,True)
	#for k in xrange(2,26):heirarchical(X,names,k)

