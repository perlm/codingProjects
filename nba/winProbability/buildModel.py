import numpy as np
import sklearn.linear_model as lm
import sklearn.cross_validation as cv
from sklearn import metrics
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import log_loss
from sklearn.metrics import mean_squared_error
import math

# Builds logistic regression models using data collected by getData.py

# Factors which could be added:
# prior to game starting: record of teams before game
# during game: possession, fouls, player minutes played
# score of game at distinct points: end of 1st, 2nd, and 3rd.

def buildLogisticRegression(data,parameters,train=True):
        X = data[:,:-1]         #all except last column
        Y = data[:,-1]
        model = lm.LogisticRegression(C=1e-4)

        if (train):
                X_train, X_test, Y_train, Y_test = cv.train_test_split(X, Y, test_size=0.25)    #randomly split into train and test
                model.fit(X_train, Y_train)
                predicted = model.predict(X_test)
                print "Linear Accuracy: ", metrics.accuracy_score(Y_test, predicted)
                predicted = model.predict_proba(X_test)
		predicted = predicted[:,1]
		Y_test[Y_test == -1] = 0
                #print "Linear log-loss: ", metrics.log_loss(Y_test, predicted)
                print "Linear MSE: ", metrics.mean_squared_error(Y_test, predicted)

	#print "Linear CV Score: ", np.mean(cv.cross_val_score(lm.LogisticRegression(),X,Y))
        model.fit(X, Y)

        #print out predictions for each possible value
        f1 = open('data/logisticRegressionLinear.data','w')
        p = model.predict_proba(parameters)         #predictions (probabilities)    
        n = np.hstack((parameters,p))
        np.savetxt(f1, n, delimiter=' ')        #plot this: plot './logisticRegression.data' u 1:2:4 w p pt 5 ps 1 palette
        f1.close()

def buildLogisticRegressionInteraction(data,parameters,train=True):
        X = data[:,:-1]         #all except last column
        Y = data[:,-1]
        poly = PolynomialFeatures(degree=2, interaction_only=True)
        model = lm.LogisticRegression(C=1e-4)

        if (train):
                X_train, X_test, Y_train, Y_test = cv.train_test_split(X, Y, test_size=0.25)    #randomly split into train and test
                X_poly = poly.fit_transform(X_train)            #rows= 1, time, score, time*score
                model.fit(X_poly, Y_train)

                X_test_poly = poly.fit_transform(X_test)
                predicted = model.predict(X_test_poly)
                print "Interaction Accuracy: ", metrics.accuracy_score(Y_test, predicted)
                predicted = model.predict_proba(X_test_poly)
                predicted = predicted[:,1]
		Y_test[Y_test == -1] = 0
                #print "Interaction log-loss: ", metrics.log_loss(Y_test, predicted)
                print "Interaction MSE: ", metrics.mean_squared_error(Y_test, predicted)

        X_poly = poly.fit_transform(X)
	#print "Interaction CV Score: ", np.mean(cv.cross_val_score(lm.LogisticRegression(),X_poly,Y))
        model.fit(X_poly, Y)

        #print out predictions for each possible value
        f1 = open('data/logisticRegressionInteraction.data','w')
        p = model.predict_proba(poly.fit_transform(parameters))         #predictions (probabilities)    
        n = np.hstack((poly.fit_transform(parameters),p))
        np.savetxt(f1, n, delimiter=' ')        #plot this: plot './logisticRegression.data' u 1:2:4 w p pt 5 ps 1 palette
        f1.close()


def buildLogisticRegressionPolynomial(data,order,parameters,train=True):
	X = data[:,:-1]		#all except last column
	Y = data[:,-1]
	poly = PolynomialFeatures(degree=order, interaction_only=False)
	model = lm.LogisticRegression(C=1e-4)

	if (train):
		X_train, X_test, Y_train, Y_test = cv.train_test_split(X, Y, test_size=0.25)	#randomly split into train and test
		X_poly = poly.fit_transform(X_train)		#rows= 1, time, score, time*score
		model.fit(X_poly, Y_train)

		X_test_poly = poly.fit_transform(X_test)
		predicted = model.predict(X_test_poly)
		print "Order-", order, "Accuracy: ", metrics.accuracy_score(Y_test, predicted)
                predicted = model.predict_proba(X_test_poly)
                predicted = predicted[:,1]
		Y_test[Y_test == -1] = 0
		#print "Order-", order, "log-loss: ", metrics.log_loss(Y_test, predicted)
		print "Order-", order, "MSE: ", metrics.mean_squared_error(Y_test, predicted)

	X_poly = poly.fit_transform(X)
	#print "Order-", order, "CV Score: ", np.mean(cv.cross_val_score(lm.LogisticRegression(),X_poly,Y))
	model.fit(X_poly, Y)
		
	#print out predictions for each possible value
	f1 = open('data/logisticRegressionPolynomial%s.data' % (order),'w')
	p = model.predict_proba(poly.fit_transform(parameters))		#predictions (probabilities)	
	n = np.hstack((poly.fit_transform(parameters),p))
	np.savetxt(f1, n, delimiter=' ')	#plot this: plot './logisticRegression.data' u 1:2:4 w p pt 5 ps 1 palette
	f1.close()

	#write out data for two individual games
	if (order == 2) and (True):
		p = model.predict_proba(poly.fit_transform(X))
		n = np.hstack((poly.fit_transform(X),p))
		writeSingleGame(n,order,0)

		Y[Y < 0] = 0
		upset = np.absolute(Y - p[:,1])
		maxUpsetIndex = np.argmax(upset)
		#maxUpset = np.amax(upset)
		writeSingleGame(n,order,maxUpsetIndex)
		


def writeSingleGame(n,order,index):
	#write out data and predictions for a game

	#col with probs = terms in bivariate polynomial + 1. (change the 2 if need multivariate)
	p = (math.factorial(order+2) / math.factorial(order) / math.factorial(2)) + 1	
	index = int(index) - int(n[index,1])	#start at beginning of game

	f1 = open('data/game_%s.data' % (index),'w')
	for x in xrange(index,index+48):f1.write('{0} {1} {2}\n'.format(n[x,1], n[x,2], n[x,p]))

def LogisticRegressionRegularization(data,order):
	#find optimal term for the inverse of regularization strength (smaller=more regularization)
	X = data[:,:-1]		#all except last column
	Y = data[:,-1]
	poly = PolynomialFeatures(degree=order, interaction_only=False)

	for reg in xrange(-5,6,1):
		regValue = 1 * 10**(reg)
		model = lm.LogisticRegression(C=regValue)

		X_train, X_test, Y_train, Y_test = cv.train_test_split(X, Y, test_size=0.25)	#randomly split into train and test
		X_poly = poly.fit_transform(X_train)		#rows= 1, time, score, time*score
		model.fit(X_poly, Y_train)

		X_test_poly = poly.fit_transform(X_test)
		predicted = model.predict(X_test_poly)
		print "reg=", reg, "Accuracy: ", metrics.accuracy_score(Y_test, predicted)
                predicted = model.predict_proba(X_test_poly)
                predicted = predicted[:,1]
		Y_test[Y_test == -1] = 0
		#print "reg=", reg, "log-loss: ", metrics.log_loss(Y_test, predicted)
		print "reg=-", reg, "MSE: ", metrics.mean_squared_error(Y_test, predicted)

	X_poly = poly.fit_transform(X)
	model.fit(X_poly, Y)
		

def buildLogisticRegressionQuarters(gameData,order, train=True):
	#this doesn't work yet
	#if i include q1 and q2 I get almost identical numbers, implying that they don't contribute...

	#reshape gameData [q1, q2, q3, w]
	#q1 = gameData[gameData[:,0] == 12][:,1]
	#q2 = gameData[gameData[:,0] == 24][:,1]
	q3 = gameData[gameData[:,0] == 36][:,1]
	w = gameData[gameData[:,0] == 12][:,-1]
	#data = np.transpose(np.vstack((q1,q2,q3,w)))
	data = np.transpose(np.vstack((q3,w)))

        #f1 = open('data/quarters.data','w')
        #np.savetxt(f1, data, delimiter=' ')
        #f1.close()

	X = data[:,:-1]		#all except last column
	Y = data[:,-1]
	poly = PolynomialFeatures(degree=order, interaction_only=False)
	model = lm.LogisticRegression(C=1e-4)

	if (train):
		X_train, X_test, Y_train, Y_test = cv.train_test_split(X, Y, test_size=0.25)	#randomly split into train and test
		X_poly = poly.fit_transform(X_train)		#rows= 1, time, score, time*score
		model.fit(X_poly, Y_train)

		X_test_poly = poly.fit_transform(X_test)
		predicted = model.predict(X_test_poly)
		print "Order-", order, "Accuracy: ", metrics.accuracy_score(Y_test, predicted)
                predicted = model.predict_proba(X_test_poly)
                predicted = predicted[:,1]
		Y_test[Y_test == -1] = 0
		#print "Order-", order, "log-loss: ", metrics.log_loss(Y_test, predicted)
		print "Order-", order, "MSE: ", metrics.mean_squared_error(Y_test, predicted)

	#X_poly = poly.fit_transform(X)
	##print "Order-", order, "CV Score: ", np.mean(cv.cross_val_score(lm.LogisticRegression(),X_poly,Y))
	#model.fit(X_poly, Y)
		
	##print out predictions for each possible value
	#f1 = open('data/logisticRegressionPolynomial%s.data' % (order),'w')
	#p = model.predict_proba(poly.fit_transform(parameters))		#predictions (probabilities)	
	#n = np.hstack((poly.fit_transform(parameters),p))
	#np.savetxt(f1, n, delimiter=' ')	#plot this: plot './logisticRegression.data' u 1:2:4 w p pt 5 ps 1 palette
	#f1.close()


if __name__ == '__main__':

	gameData = np.loadtxt('data/gameData_all.data', dtype=int)

	#parameters = np.transpose([np.tile(np.arange(0,48), len(np.arange(-50,51))), np.repeat(np.arange(-50,51), len(np.arange(0,48)))])
	##compare polynomial order
        #buildLogisticRegression(gameData,parameters,True)
	#buildLogisticRegressionInteraction(gameData,parameters,True)
	#for order in xrange(2,6):
	#	buildLogisticRegressionPolynomial(gameData, order,parameters,True)

	#find regularization
	#LogisticRegressionRegularization(gameData,2)

	for  order in xrange(2,6):
		buildLogisticRegressionQuarters(gameData,order,True)


