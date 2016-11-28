#!/usr/bin/python

# so this will be the master

from getData import *
from buildModel import *
from tweetIt import *

def main():

	# download 
	#getRawData()

	# model - df is from file. df2 is with features. x, scaled, fixed are after processing.
        d = readRawFile()
        d2 = constructFeatures(d)
        X, X_scaled, Y, scaler, X_fix = processData(d2)
        model = buildLogisticModel(X_scaled,Y,X_fix)

	# predict - df3 is with additional row for predictions. then process in exact same way.
	features = getCurrentStatus()
	d3 = addRow(d,features)
        d4 = constructFeatures(d3)
        X, X_scaled, Y, scaler, X_fix = processData(d4,scaler)
	prob = predict(X_scaled,model)
	features['prob'] = prob

	# tweet it!
	tweetProb(features)



if __name__ == "__main__":
	main()
