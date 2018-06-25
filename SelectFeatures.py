import subprocess
import operator
import numpy as np
import os
import pandas as pd
import ResAnaylsis
import FeatureSelectionUtillFunctions as fsutill
import multiprocessing as mp



def DoubleCrossValEvaluation(MetaboDataStructure,outerN,innerN,NumFeatures,FunctionToSelect,FunctionToMergeSelected,FunctionToEvaluate,Results):
    outerFolds = MetaboDataStructure.getNFolds(outerN,True)

    OuterFoldSelected = []
    OuterFoldTest = []
    
    for OuterTrain, Validate in outerFolds:
        innerCrossFolds = OuterTrain.getNFolds(innerN,False)
        ListOfSelectedVairbles = []
        ListOfEvaluation = []
        for innerTrain, innerTest in innerCrossFolds:
            Selected = FunctionToSelect(innerTrain,NumFeatures)
            ListOfSelectedVairbles.append(Selected)
            ListOfEvaluation.append(FunctionToEvaluate(innerTrain,innerTest,getListOfSelected(Selected)))
        OuterMerged = FunctionToMergeSelected(ListOfSelectedVairbles,ListOfEvaluation,NumFeatures,True,False)
        OuterFoldSelected.append(OuterMerged)
        OuterFoldTest.append(FunctionToEvaluate(OuterTrain,Validate,getListOfSelected(OuterMerged))) 
    
    FinalSelection = FunctionToMergeSelected(OuterFoldSelected,OuterFoldTest,NumFeatures,False,False)
    
    Results["FinalSelection"] = FinalSelection
    Results["OuterFoldTest"] = OuterFoldTest
    return Results


def EvaluateSelectionWithDoubleCFV(MetaboDataStructure,NumRepeat,NumCores,outerN,innerN,NumFeatures, FunctionToSelect,FunctionToMergeSelected,FunctionToEvaluate):
    manager = mp.Manager()
    ListOFSelectedFeatures = []
    ListofFitness = [] 
    for i in range(int(NumRepeat/NumCores)):
         TmpList = []
         if i == 1 - int(NumRepeat/NumCores):
             TmpList = [manager.dict() for i in range(NumCores - (NumRepeat % NumCores))]
             CreateRunProcess(MetaboDataStructure,NumCores - (NumRepeat % NumCores),outerN,innerN,NumFeatures, FunctionToSelect,FunctionToMergeSelected,FunctionToEvaluate,TmpList)
         else:
             TmpList = [manager.dict() for i in range(NumCores)]
             CreateRunProcess(MetaboDataStructure,NumCores,outerN,innerN,NumFeatures, FunctionToSelect,FunctionToMergeSelected,FunctionToEvaluate,TmpList)
         ListOFSelectedFeatures += [CoreResCoreRes["FinalSelection"] for CoreResCoreRes in TmpList]
         ListofFitness.extend([CoreResCoreRes["OuterFoldTest"] for CoreResCoreRes in TmpList])
    
    TotalSelection = FunctionToMergeSelected(ListOFSelectedFeatures,ListofFitness,NumFeatures,False,True)
    DictOfFitness = fsutill.ConvertListOfDictsToDictOfLists(ListofFitness[0])
    AVGSTDFitness = {}
    for ResType in DictOfFitness:
        AVGSTDFitness[ResType] = {"Mean": np.mean(DictOfFitness[ResType]),"STD": np.std(DictOfFitness[ResType])}
    
    return {"TotalSelection": TotalSelection, "AVGSTDFitness": AVGSTDFitness}
        

def CreateRunProcess(MetaboDataStructure,NumCores,outerN,innerN,NumFeatures, FunctionToSelect,FunctionToMergeSelected,FunctionToEvaluate,Results):
    processes = [mp.Process(target=DoubleCrossValEvaluation, args=(MetaboDataStructure,outerN,innerN,NumFeatures,FunctionToSelect,FunctionToMergeSelected,FunctionToEvaluate,Results[i])) for i in range(NumCores)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    return

def getListOfSelected(StructureOfNames):
    if(type(StructureOfNames) is (pd.DataFrame or pd.Series)):
        return list(StructureOfNames.index)
    elif (type(StructureOfNames) is list):
        return StructureOfNames
    elif (type(StructureOfNames) is dict):
        return list(StructureOfNames.keys())
    return -1
             

