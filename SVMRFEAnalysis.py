import MetFileParser
import SelectFeatures
import multiprocessing as mp
import pandas as pd
import ResAnaylsis
import FeatureSelectionUtillFunctions as fsutill
import numpy as np
import os
import operator
from sklearn.svm import SVR
from sklearn.svm import SVC
from sklearn.feature_selection import RFE




def EvaluateClassSVM(Train,Test,Selected):
    
    
    FunctionToEvaluate = lambda ident: 1 if 13 <= int(ident.split("-")[0]) <= 39 else 0 
    
    XYTrain = Train.getConditionAndFeatures(FunctionToEvaluate,Selected)
    XYTes = Test.getConditionAndFeatures(FunctionToEvaluate,Selected)
    
    x_Data_Train = XYTrain['x_Data']
    y_Data_Train = XYTrain['y_Data']
    x_Data_Test  = XYTes['x_Data']
    y_Data_Test  = XYTes['y_Data']
    
    XYTrain = Train.getConditionAndFeatures(FunctionToEvaluate,Selected)
    
    
    Class_SVM = SVC(kernel="linear").fit(MetFileParser.ParetoScale(x_Data_Train),y_Data_Train)
    SVMRes = Class_SVM.predict(x_Data_Test)
    FalsePositive = ResAnaylsis.getFalsePositiveRate(SVMRes,y_Data_Test)
    TruePositive = ResAnaylsis.getTruePositiveRate(SVMRes,y_Data_Test)
    CorrectClassificationRate = ResAnaylsis.getCorrectClassificationRate(SVMRes,y_Data_Test)
    return {"FalsePositive": FalsePositive, "TruePositive": TruePositive, "CorrectClassificationRate": CorrectClassificationRate,"y_Test_Pedict": {"y_Data_Test": y_Data_Test, "y_Predict": SVMRes}}


    
def EvaluateRegresionSVM(Train,Test,Selected):
    
    yTemplate = {1 : 0, 2 : 1, 3 : 1.5, 4 : 2, 5 : 2.5, 6 : 3, 7 : 4, 8 : 6, 9 : 8, 10 : 10, 11 : 12, 12 : 13, 13 : 13.5, 14 : 14, 15 : 14.5, 16 : 15,17 : 16, 18 : 18, 19 : 20, 20 : 22, 21 : 24, 22 : 25, 23 : 25.5, 24 : 26} 
    FunctionToEvaluate = lambda ident: yTemplate[int(int(float(ident.split("-")[0])-1)/3) + 1]
    
    XYTrain = Train.getConditionAndFeatures(FunctionToEvaluate,Selected)
    XYTes = Test.getConditionAndFeatures(FunctionToEvaluate,Selected)
    
    x_Data_Train = XYTrain['x_Data']
    y_Data_Train = XYTrain['y_Data']
    x_Data_Test  = XYTes['x_Data']
    y_Data_Test  = XYTes['y_Data']
    
    Class_SVM = SVR(kernel="linear").fit(MetFileParser.ParetoScale(x_Data_Train),y_Data_Train)
    
    SVMRes = Class_SVM.predict(x_Data_Test)
    RMSE = ResAnaylsis.getRMSE(SVMRes,y_Data_Test)
    Qsqd = ResAnaylsis.getQsqrd(SVMRes,y_Data_Test)
    return {"RMSE": RMSE, "Qsqd": Qsqd, "y_Test_Pedict": {"y_Data_Test": y_Data_Test, "y_Predict": SVMRes}}

def SelectWithSVMClass(DataStructure,N):
    FunctionToEvaluate = lambda ident: 1 if 13 <= int(ident.split("-")[0]) <= 39 else 0 
    XY = DataStructure.getConditionAndFeatures(FunctionToEvaluate)
    x_Data = XY['x_Data']
    y_Data = XY['y_Data']
    CompTestImportance = getSVMResults(x_Data,y_Data,N,Mode = "Class")
    fsutill.ChangeIndName(CompTestImportance,DataStructure.getListOfMetabolites())
    return CompTestImportance

def SelectWithSVMRegresion(DataStructure,N):
    yTemplate = {1 : 0, 2 : 1, 3 : 1.5, 4 : 2, 5 : 2.5, 6 : 3, 7 : 4, 8 : 6, 9 : 8, 10 : 10, 11 : 12, 12 : 13, 13 : 13.5, 14 : 14, 15 : 14.5, 16 : 15,17 : 16, 18 : 18, 19 : 20, 20 : 22, 21 : 24, 22 : 25, 23 : 25.5, 24 : 26} 
    FunctionToEvaluate = lambda ident: yTemplate[int(int(float(ident.split("-")[0])-1)/3) + 1]
    XY = DataStructure.getConditionAndFeatures(FunctionToEvaluate)
    x_Data = XY['x_Data']
    y_Data = XY['y_Data']
    CompTestImportance = getSVMResults(x_Data,y_Data,N,Mode = "Regression")
    fsutill.ChangeIndName(CompTestImportance,DataStructure.getListOfMetabolites())
    return CompTestImportance



def getSVMResults(x_Data,y_Data,N,Scaling = "Pareto",Mode = "Class"):
    
    if(Scaling == "Pareto"):
        x_Data = MetFileParser.ParetoScale(x_Data)
    
    if (Mode == "Class"):
        Class_SVM = SVC(kernel="linear")
        Class_RFE = RFE(Class_SVM, N, step=5)
        Class_RFE = Class_RFE.fit(x_Data,y_Data)
        
        Top100_Class = []
        for i in range(len(Class_RFE.ranking_)):
            if(Class_RFE.ranking_[i] == 1):
                Top100_Class.append("X"+ str(i + 1))
        return Top100_Class
    
    elif (Mode == "Regression"):
          REG_SVM   = SVR(kernel="linear")
          REG_RFE   = RFE(REG_SVM, N, step=5)   
          REG_RFE   = REG_RFE.fit(x_Data,y_Data)
    
          Top100_REG = []
          for i in range(len(REG_RFE.ranking_)):
            if(REG_RFE.ranking_[i] == 1):
                Top100_REG.append("X"+ str(i + 1))
          return Top100_REG
    return -1

def MergeSVMClass(ListOfSelected,ListOfEvaluation,N,InteriorMerge,FinalMerge):
    
    if(InteriorMerge):
        BestQsqd  = 0
        BestSelect = []
        for i in range(len(ListOfEvaluation)):
            if(BestQsqd < ListOfEvaluation[i]["CorrectClassificationRate"]):
               BestQsqd = ListOfEvaluation[i]["CorrectClassificationRate"]
               BestSelect = ListOfSelected[i]
        return BestSelect
    
    DictOfSelected = {}
    for Selects in ListOfSelected:
        for Selected in Selects:
            if(DictOfSelected.get(Selected) == None):
                DictOfSelected[Selected] = 1
            else:
                DictOfSelected[Selected] += 1
    SortSelected = sorted(DictOfSelected.items(), key=operator.itemgetter(1))
    Selected = SortSelected[:N]
    MergedResults = [res[0] for res in Selected]
    
    if(not FinalMerge):
        return MergedResults
    
    return pd.DataFrame(data=Selected)

def MergeSVMReg(ListOfSelected,ListOfEvaluation,N,InteriorMerge,FinalMerge):
    if(InteriorMerge):
        BestRMSE  = 999999999999
        BestSelect = []
        for i in range(len(ListOfEvaluation)):
            if(BestRMSE > ListOfEvaluation[i]["RMSE"]):
               BestRMSE = ListOfEvaluation[i]["RMSE"]
               BestSelect = ListOfSelected[i]
        return BestSelect
    
    DictOfSelected = {}
    for Selects in ListOfSelected:
        for Selected in Selects:
            if(DictOfSelected.get(Selected) == None):
                DictOfSelected[Selected] = 1
            else:
                DictOfSelected[Selected] += 1
    
    SortSelected = sorted(DictOfSelected.items(), key=operator.itemgetter(1))
    Selected = SortSelected[:N]
    MergedResults = [res[0] for res in Selected]
    
    if(not FinalMerge):
        return MergedResults
    
    return pd.DataFrame(data=Selected)

def MergeResultsWraper(ListOfSelected,ListOfEvaluation,N,InteriorMerge,FinalMerge):
    
    if(FinalMerge):
        DictOfSelected = {}
        for Selects in ListOfSelected:
            for Selected in Selects:
                if(DictOfSelected.get(Selected) == None):
                    DictOfSelected[Selected] = 1
                else:
                    DictOfSelected[Selected] += 1
        SortSelected = sorted(DictOfSelected.items(), key=operator.itemgetter(1))
        Selected = SortSelected[:N]
        MergedResults = [res[0] for res in Selected]
        if(not InteriorMerge):
            return pd.DataFrame(data=Selected)
        return MergedResults
    else:
        ret = []
        for selects in ListOfSelected:
            for met in selects:
                ret.append(met)
        return ret
            



        
    
    
    
    
