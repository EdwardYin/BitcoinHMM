import csv
import random
import math
import pandas as pd
import numpy as np

class Preprocess():
    # discretize the raw data set
    # make number of states completely dynamic
    # use an array input to define thresholds for states
    # store numStates as a variable in class
    # intended to use as direct input to the createTransitionMatrix function
    # also intended to replaced discretizeData function

    def __init__(self, thresholdArray, rawDataArray):
        self.numStates = len(rawDataArray)

def discretizeData(inArray):
    threshold = .0025
    # Assume 3 states for now
    outArray = np.empty(len(inArray)-1)
    for i in range (0, len(inArray)-1):
        if float(inArray[i])/float(inArray[i+1]) - 1 < -1*threshold:
            outArray[i] = int(0)
        elif float(inArray[i])/float(inArray[i+1]) - 1 > threshold:
            outArray[i] = int(2)
        else:
            outArray[i] = int(1)
    return outArray

def createTransitionMatrix(inArray, keyLength, numStates):
    #inArray is an array of discretized Data, 0 through n for number of states
    if numStates < 2:
        return "Must have at least 2 states in transition matrix"
    if keyLength < 1:
        return "Key must be integer >= 1"

    rows = pow(numStates,keyLength)
    columns = numStates
    tMatrix = np.empty((rows, columns))
    countMatrix = np.empty((rows, columns))
    tMatrix.fill(0)
    countMatrix.fill(0)

    maxLen = len(inArray) - keyLength - 1
    for i in range(0,maxLen):
        # for each starting point, first n states go into key
        # concatenate into string the first n states into string
        keyStr = ""
        for j in range(0, keyLength):
            keyStr = keyStr + str(int(inArray[i+j]))
            if i<5:
                print("string: " + keyStr)

        # turn this into binary for array index
        index = int(keyStr, numStates)

        countMatrix[index][int(inArray[i+keyLength])] = countMatrix[index][int(inArray[i+keyLength])] + 1

    #populate transition matrix using the count matrix
    for i in range(0, rows):
        for j in range(0, columns):
            tMatrix[i][j] = countMatrix[i][j]/np.sum(countMatrix[i])

    return tMatrix

if __name__ in '__main__':
    # reads this CSV file into a DataFrame
    csvPath = 'C:\\Users\\Edward\\Documents\\Github\\BitcoinHMM\\vwapHourlyBTCUSD.csv'
    myDF = pd.read_csv(csvPath)
    dArray = discretizeData(myDF['Vwap'])
    endMatrix = createTransitionMatrix(dArray, 3, 3)
    print(endMatrix)
    # createTransitionMatrix(myDF, 3)
