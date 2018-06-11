import csv
import numpy as np

def GetTreeResults(FileName):
    ret = []
    First = True
    with open(FileName, 'rt') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row is not None:
                if(First):
                    First = False
                else:
                    ret.append(float(row[1]))
    return ret
    
def getRMSE(yRes,yTest):
    totSE = 0
    for i in range(len(yRes)):
        totSE = totSE + (yRes[i]- yTest[i])**2
    MSE = totSE / len(yRes)
    RMSE = MSE**.5
    return RMSE

def getFalsePositiveRate(yRes,yTest):
    FalsePos = 0
    count = 0
    for i in range(len(yRes)):
        if(yRes[i] == 0):
            if (yRes[i] == yTest[i]):
                FalsePos = FalsePos + 1
            count =  count + 1
    if count == 0:
        return np.NaN
    FalsePosRate = FalsePos / count
    return FalsePosRate
    
def getTruePositiveRate(yRes,yTest):
    TruePos = 0
    count = 0
    for i in range(len(yRes)):
        if(yRes[i] == 1):
            if(yRes[i] == yTest[i]):
                TruePos = TruePos + 1
            count = count + 1
    if count == 0:
        return np.NaN
    TruePosRate = TruePos / count
    return TruePosRate