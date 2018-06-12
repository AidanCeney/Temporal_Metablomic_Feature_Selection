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
            ListOfEvaluation.append(FunctionToEvaluate(innerTrain,innerTest,list(Selected.index)))
        OuterMerged = FunctionToMergeSelected(ListOfSelectedVairbles,NumFeatures,True)
        OuterFoldSelected.append(OuterMerged)
        OuterFoldTest.append(FunctionToEvaluate(OuterTrain,Validate,list(OuterMerged.index))) 
    
    FinalSelection = FunctionToMergeSelected(OuterFoldSelected,NumFeatures,True)
    
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
    
    TotalSelection = FunctionToMergeSelected(ListOFSelectedFeatures,NumFeatures,False)
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
             
def MergeResultsWraper(ListOfSelected,N):
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
    return MergedResults
    
def MergeResultsVIPImp(ListOfSelected,N):
    CombinedDataFrame = pd.concat(ListOfSelected, axis=1)
    CombinedDataFrame['Mean'] = CombinedDataFrame.mean(axis=1)
    CombinedDataFrame['STD'] = CombinedDataFrame.std(axis=1)
    CombinedDataFrame = CombinedDataFrame.sort_values(by=["Mean"],ascending=False).head(N)
    CombinedDataFrame = CombinedDataFrame[["Mean","STD"]]
    CombinedDataFrame = CombinedDataFrame.rename(columns={'Mean': 'VarImp'})
    return CombinedDataFrame
    

