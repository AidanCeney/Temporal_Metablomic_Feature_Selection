import MetFileParser
import SelectFeatures
import multiprocessing as mp
import pandas as pd
import ResAnaylsis
import FeatureSelectionUtillFunctions as fsutill
import numpy as np
import os
import operator


def EvaluateClassRF(Train,Test,Selected):
    
    FunctionToEvaluate = lambda ident: 1 if 13 <= int(ident.split("-")[0]) <= 39 else 0 

    XYTrain = Train.getConditionAndFeatures(FunctionToEvaluate,Selected)
    XYTes = Test.getConditionAndFeatures(FunctionToEvaluate,Selected)
    
    x_Data_Train = XYTrain['x_Data']
    y_Data_Train = XYTrain['y_Data']
    x_Data_Test  = XYTes['x_Data']
    y_Data_Test  = XYTes['y_Data']
    
    np.savetxt('Fold/x_Data_Train_' + str(os.getpid()) +'.csv',x_Data_Train,delimiter  =",")
    np.savetxt('Fold/y_Data_Train_' + str(os.getpid()) +'.csv',y_Data_Train,delimiter  =",")
    np.savetxt('Fold/x_Data_Test_'  + str(os.getpid())  +'.csv',x_Data_Test,delimiter  =",")
    fsutill.TestRF()
    RFRes = pd.read_csv("Fold/y_Test_Res_RF_" + str(os.getpid()) + ".csv",index_col = 0)
    RFRes = list(RFRes.mean(1).values)
    FalsePositive = ResAnaylsis.getFalsePositiveRate(RFRes, y_Data_Test)
    TruePositive  = ResAnaylsis.getTruePositiveRate(RFRes  , y_Data_Test)
    CorrectClassificationRate = ResAnaylsis.getCorrectClassificationRate(RFRes,y_Data_Test)
    return {"FalsePositive": FalsePositive, "TruePositive": TruePositive, "CorrectClassificationRate": CorrectClassificationRate, "y_Test_Pedict": {"y_Data_Test": y_Data_Test, "y_Predict": RFRes}}



    
def EvaluateRegresionRF(Train,Test,Selected):
    
    yTemplate = {1 : 0, 2 : 1, 3 : 1.5, 4 : 2, 5 : 2.5, 6 : 3, 7 : 4, 8 : 6, 9 : 8, 10 : 10, 11 : 12, 12 : 13, 13 : 13.5, 14 : 14, 15 : 14.5, 16 : 15,17 : 16, 18 : 18, 19 : 20, 20 : 22, 21 : 24, 22 : 25, 23 : 25.5, 24 : 26} 
    FunctionToEvaluate = lambda ident: yTemplate[int(int(float(ident.split("-")[0])-1)/3) + 1]
    
    XYTrain = Train.getConditionAndFeatures(FunctionToEvaluate,Selected)
    XYTes = Test.getConditionAndFeatures(FunctionToEvaluate,Selected)
    
    x_Data_Train = XYTrain['x_Data']
    y_Data_Train = XYTrain['y_Data']
    x_Data_Test  = XYTes['x_Data']
    y_Data_Test  = XYTes['y_Data']
    
    np.savetxt('Fold/x_Data_Train_' + str(os.getpid()) +'.csv',x_Data_Train,delimiter =",")
    np.savetxt('Fold/y_Data_Train_' + str(os.getpid()) +'.csv',y_Data_Train,delimiter =",")
    np.savetxt('Fold/x_Data_Test_' + str(os.getpid())  +'.csv',x_Data_Test,delimiter  =",")
    fsutill.TestRF()
    RFRes = pd.read_csv("Fold/y_Test_Res_RF_" + str(os.getpid()) + ".csv",index_col = 0)
    RFRes = list(RFRes.mean(1).values)
    RMSE = ResAnaylsis.getRMSE(RFRes,y_Data_Test)
    Qsqd = ResAnaylsis.getQsqrd(RFRes,y_Data_Test)
    return {"RMSE": RMSE, "Qsqd": Qsqd, "y_Test_Pedict": {"y_Data_Test": y_Data_Test, "y_Predict": RFRes}}


def SelectWithVitaClass(DataStructure,N):
    FunctionToEvaluate = lambda ident: 1 if 13 <= int(ident.split("-")[0]) <= 39 else 0 
    XY = DataStructure.getConditionAndFeatures(FunctionToEvaluate)
    np.savetxt('TmpFiles/x_Data_Train_' + str(os.getpid()) +'.csv', XY['x_Data'],delimiter =",")
    np.savetxt('TmpFiles/y_Data_Train_' + str(os.getpid()) +'.csv', XY['y_Data'],delimiter =",")
    fsutill.RFVita()
    CompTestImportance = fsutill.getDataFrameOfVarImp("TmpFiles/VitaNSelected" + str(os.getpid()) + ".csv").sort_values(by=["VarImp"],ascending=False)
    fsutill.ChangeIndName(CompTestImportance,DataStructure.getListOfMetabolites())
    return CompTestImportance

def SelectWithPIMPRegresion(DataStructure,N):
    yTemplate = {1 : 0, 2 : 1, 3 : 1.5, 4 : 2, 5 : 2.5, 6 : 3, 7 : 4, 8 : 6, 9 : 8, 10 : 10, 11 : 12, 12 : 13, 13 : 13.5, 14 : 14, 15 : 14.5, 16 : 15,17 : 16, 18 : 18, 19 : 20, 20 : 22, 21 : 24, 22 : 25, 23 : 25.5, 24 : 26} 
    FunctionToEvaluate = lambda ident: yTemplate[int(int(float(ident.split("-")[0])-1)/3) + 1]
    XY = DataStructure.getConditionAndFeatures(FunctionToEvaluate)
    np.savetxt('TmpFiles/x_Data_Train_' + str(os.getpid()) +'.csv', XY['x_Data'],delimiter =",")
    np.savetxt('TmpFiles/y_Data_Train_' + str(os.getpid()) +'.csv', XY['y_Data'],delimiter =",")
    fsutill.RFPIMP()
    CompTestImportance = fsutill.getDataFrameOfVarImp("TmpFiles/PimpNSelected" + str(os.getpid()) + ".csv").sort_values(by=["VarImp"],ascending=False)
    fsutill.ChangeIndName(CompTestImportance,DataStructure.getListOfMetabolites())
    return CompTestImportance

def SelectWithPIMPClass(DataStructure,N):
    FunctionToEvaluate = lambda ident: 1 if 13 <= int(ident.split("-")[0]) <= 39 else 0 
    XY = DataStructure.getConditionAndFeatures(FunctionToEvaluate)
    np.savetxt('TmpFiles/x_Data_Train_' + str(os.getpid()) +'.csv', XY['x_Data'],delimiter =",")
    np.savetxt('TmpFiles/y_Data_Train_' + str(os.getpid()) +'.csv', XY['y_Data'],delimiter =",")
    fsutill.RFPIMP()
    CompTestImportance = fsutill.getDataFrameOfVarImp("TmpFiles/PimpNSelected" + str(os.getpid()) + ".csv").sort_values(by=["VarImp"],ascending=False)
    fsutill.ChangeIndName(CompTestImportance,DataStructure.getListOfMetabolites())
    return CompTestImportance

def SelectWithVitaRegresion(DataStructure,N):
    yTemplate = {1 : 0, 2 : 1, 3 : 1.5, 4 : 2, 5 : 2.5, 6 : 3, 7 : 4, 8 : 6, 9 : 8, 10 : 10, 11 : 12, 12 : 13, 13 : 13.5, 14 : 14, 15 : 14.5, 16 : 15,17 : 16, 18 : 18, 19 : 20, 20 : 22, 21 : 24, 22 : 25, 23 : 25.5, 24 : 26} 
    FunctionToEvaluate = lambda ident: yTemplate[int(int(float(ident.split("-")[0])-1)/3) + 1]
    XY = DataStructure.getConditionAndFeatures(FunctionToEvaluate)
    np.savetxt('TmpFiles/x_Data_Train_' + str(os.getpid()) +'.csv', XY['x_Data'],delimiter =",")
    np.savetxt('TmpFiles/y_Data_Train_' + str(os.getpid()) +'.csv', XY['y_Data'],delimiter =",")
    fsutill.RFVita()
    CompTestImportance = fsutill.getDataFrameOfVarImp("TmpFiles/VitaNSelected" + str(os.getpid()) + ".csv").sort_values(by=["VarImp"],ascending=False)
    fsutill.ChangeIndName(CompTestImportance,DataStructure.getListOfMetabolites())
    return CompTestImportance

def MergeResultsVIPImp(ListOfSelected,ListOfEvaluation,N,InteriorMerge,FinalMerge):
    CombinedDataFrame = pd.concat(ListOfSelected, axis=1)
    CombinedDataFrame['Mean'] = CombinedDataFrame.mean(axis=1)
    CombinedDataFrame['STD'] = CombinedDataFrame.std(axis=1)
    CombinedDataFrame = CombinedDataFrame.sort_values(by=["Mean"],ascending=False).head(N)
    CombinedDataFrame = CombinedDataFrame[["Mean","STD"]]
    CombinedDataFrame = CombinedDataFrame.rename(columns={'Mean': 'VarImp'})
    if (not FinalMerge):
        CombinedDataFrame = CombinedDataFrame.drop(columns = ['STD'])
        return CombinedDataFrame
    return CombinedDataFrame.head(N)


        
    
    
    
    