import subprocess
import operator
import numpy as np
import os
import pandas as pd
import ResAnaylsis
import FeatureSelectionUtillFunctions as fsutill
import multiprocessing as mp



def DoubleCrossValEvaluation(MetaboDataStructure,outerN,innerN,FunctionToSelect,FunctionToMergeSelected,FunctionToEvaluate,Results):
    outerFolds = MetaboDataStructure.getNFolds(outerN,True)

    OuterFoldSelected = []
    OuterFoldTest = []
    
    for OuterTrain, Validate in outerFolds:
        innerCrossFolds = OuterTrain.getNFolds(innerN,False)
        ListOfSelectedVairbles = []
        ListOfEvaluation = []
        for innerTrain, innerTest in innerCrossFolds:
            Selected = FunctionToSelect(innerTrain,100)
            ListOfSelectedVairbles.append(Selected)
            ListOfEvaluation.append(FunctionToEvaluate(innerTrain,innerTest,list(Selected.index)))
        OuterMerged = FunctionToMergeSelected(ListOfSelectedVairbles,len(OuterTrain.getListOfMetabolites()))
        OuterFoldSelected.append(OuterMerged)
        OuterFoldTest.append(FunctionToEvaluate(OuterTrain,Validate,list(OuterMerged.index))) 
    SelectedWithoutSTD = []
    for frame in OuterFoldSelected:
        SelectedWithoutSTD.append(frame.drop(columns = ['STD']))
    FinalSelection = FunctionToMergeSelected(SelectedWithoutSTD,len(OuterTrain.getListOfMetabolites()))
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
             CreateRunProcess(MetaboDataStructure,NumCores,outerN,innerN,NumFeatures, FunctionToSelect,FunctionToMergeSelected,FunctionToEvaluate,Results)
         ListOFSelectedFeatures += [CoreResCoreRes["FinalSelection"] for CoreResCoreRes in TmpList]
         ListofFitness.extend([CoreResCoreRes["OuterFoldTest"] for CoreResCoreRes in TmpList])
    
    SelectedWithoutSTD = []
    for frame in ListOFSelectedFeatures:
        SelectedWithoutSTD.append(frame.drop(columns = ['STD']))
    
    TotalSelection = FunctionToMergeSelected(SelectedWithoutSTD,NumFeatures)
    DictOfFitness = fsutill.ConvertListOfDictsToDictOfLists(ListofFitness[0])
    AVGSTDFitness = {}
    for ResType in DictOfFitness:
        AVGSTDFitness[ResType] = {"Mean": np.mean(DictOfFitness[ResType]),"STD": np.std(DictOfFitness[ResType])}
    
    return {"TotalSelection": TotalSelection, "AVGSTDFitness": AVGSTDFitness}
        

def CreateRunProcess(MetaboDataStructure,NumCores,outerN,innerN,NumFeatures, FunctionToSelect,FunctionToMergeSelected,FunctionToEvaluate,Results):
    processes = [mp.Process(target=DoubleCrossValEvaluation, args=(MetaboDataStructure,outerN,innerN,FunctionToSelect,FunctionToMergeSelected,FunctionToEvaluate,Results[i])) for i in range(NumCores)]
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
    CombinedDataFrame = pd.concat(ListOfSelected, axis=1,sort=False)
    CombinedDataFrame['Mean'] = CombinedDataFrame.mean(axis=1)
    CombinedDataFrame['STD'] = CombinedDataFrame.std(axis=1)
    CombinedDataFrame = CombinedDataFrame.sort_values(by=["Mean"],ascending=False).head(N)
    CombinedDataFrame = CombinedDataFrame[["Mean","STD"]]
    CombinedDataFrame = CombinedDataFrame.rename(columns={'Mean': 'VarImp'})
    return CombinedDataFrame
    

