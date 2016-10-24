import numpy as np
import math
from sklearn import linear_model, ensemble, cross_validation, metrics, preprocessing
#import matplotlib.pyplot as plt

def buildLogisticRegression(X, X_scaled, Y, parameters, parameters_scaled, scaler, train=True):
        model = linear_model.LogisticRegression(C=1e4)
        if (train):
                X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X_scaled, Y, test_size=0.25)    #randomly split into train and test
                model.fit(X_train, Y_train)
                predicted = model.predict(X_test)
                print "Linear Accuracy: ", metrics.accuracy_score(Y_test, predicted)
                predicted = model.predict_proba(X_test)
                predicted = predicted[:,1]
                Y_test[Y_test == -1] = 0
                print "Linear MSE: ", metrics.mean_squared_error(Y_test, predicted)

        model.fit(X_scaled, Y)
        print "Linear Logistic score", model.score(X_scaled, Y)
	print "Linear Logistic coeff", model.coef_

        f1 = open('data/logisticRegressionLinear.data','w')
        p = model.predict_proba(parameters_scaled)         #predictions (probabilities)    
        n = np.hstack((parameters,p))
        np.savetxt(f1, n, delimiter=' ')        #plot this: plot './logisticRegression.data' u 1:2:4 w p pt 5 ps 1 palette
        f1.close()

def buildLogisticRegressionPolynomial(order=3,train=True,champDays=None,champTotal=None):
	X,X_scaled, Y, parameters, parameters_scaled, scaler = processData()

	poly = preprocessing.PolynomialFeatures(degree=order, interaction_only=False)
        model = linear_model.LogisticRegression(C=1e4)
        if (train):
                X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X_scaled, Y, test_size=0.25)    #randomly split into train and test

                X_poly = poly.fit_transform(X_train)            #rows= 1, time, score, time*score
                model.fit(X_poly, Y_train)
                X_test_poly = poly.fit_transform(X_test)
                predicted = model.predict(X_test_poly)
                #print "Order-", order, "Accuracy: ", metrics.accuracy_score(Y_test, predicted)
                predicted = model.predict_proba(X_test_poly)
                predicted = predicted[:,1]
                Y_test[Y_test == -1] = 0
                #print "Order-", order, "MSE: ", metrics.mean_squared_error(Y_test, predicted)

        X_poly = poly.fit_transform(X_scaled)
        model.fit(X_poly, Y)
        print "Order", order, "Logistic score", model.score(X_poly, Y)
	#print "Order", order, "Logistic coeff", model.coef_

	if (not champDays) or (not champTotal):
	        f1 = open('data/logisticRegressionPolynomial%s.data' % (order),'w')
		p = model.predict_proba(poly.fit_transform(parameters_scaled))         #predictions (probabilities)    
		n = np.hstack((poly.fit_transform(parameters),p))
		np.savetxt(f1, n, delimiter=' ')        #plot this: plot './logisticRegression.data' u 1:2:4 w p pt 5 ps 1 palette
		f1.close()
	else:
		#normalize 
		toPredict = scaler.transform(np.array([champDays,champTotal]))
                toPredictPoly = poly.fit_transform(toPredict)
                predict = model.predict_proba(toPredictPoly)
		return predict[0][0]


def buildForrestRegression(X,Y,train=False):
        model = ensemble.RandomForestRegressor(n_estimators=100)
        #model = ensemble.ExtraTreesRegressor(n_estimators=500,max_depth=None)
        model.fit(X, Y)
        print "Forrest", model.score(X, Y)
	print "Forrest", model.feature_importances_

        f1 = open('data/forest.data','w')
        p = model.predict(parameters)         #predictions (probabilities)    
	print p.shape, parameters.shape
        n = np.hstack((parameters,np.reshape(p,(1000,1))))
        np.savetxt(f1, n, delimiter=' ')        #plot this: plot './logisticRegression.data' u 1:2:4 w p pt 5 ps 1 palette
        f1.close()


def nullModel(winner):
	probChampion = 1- np.mean(winner)
	print "Expect 0.33", "Found=",probChampion

def processData():
	#g, gameNumber, date, winningDays, winningDollars, winner, maxScore, players[win]
	gameData = np.genfromtxt('data/raw.data')
	Y = gameData[:,5]-1

        #First - imputation... no need here.

        #Second - standardize the dataset! mean=0, var=1...
	prevWins = gameData[:,3]
	totalPrevDollars = gameData[:,4]
	avePrevDollars = totalPrevDollars/prevWins
	X = np.matrix.transpose(np.vstack((prevWins, totalPrevDollars)))
	#X_scaled = preprocessing.scale(X)
	scaler = preprocessing.StandardScaler().fit(X)	#this allows me to re-use the scaler...
	X_scaled = scaler.transform(X) 
	parameters = np.transpose([np.tile(np.arange(0,10,1), len(np.arange(0,200000,5000))), np.repeat(np.arange(0,200000,5000), len(np.arange(0,10,1)))])
	parameters_scaled = scaler.transform(parameters) 
	return X,X_scaled, Y, parameters, parameters_scaled, scaler

if __name__ == '__main__':

	X, X_scaled, Y, parameters, parameters_scaled, scaler = processData()

	nullModel(Y)
        buildLogisticRegression(X, X_scaled, Y, parameters, parameters_scaled, scaler, True)
	for n in xrange(1,6):buildLogisticRegressionPolynomial(n,True)
        #buildForrestRegression(X,Y,False)

