import pandas as pd
from random import shuffle
import numpy as np

class MetDataStructure:
    
    def __init__(self):
        self._DictOfSamples = {}
        self._ListOfIdentifiers = []
        self._ListOfMetabolites = []

    
    def addSample(self,SampleIdentifiers,SampleMetaboliteProfile):
        if(self._DictOfSamples.get(SampleIdentifiers) !=  None):
            self._DictOfSamples[SampleIdentifiers] = {**self._DictOfSamples[SampleIdentifiers], **SampleMetaboliteProfile}
            return
        self._DictOfSamples[SampleIdentifiers] = SampleMetaboliteProfile
        self._ListOfIdentifiers.append(SampleIdentifiers)
        return
    def upDateMetabolites(self):
        for sample in self._DictOfSamples:
            self._ListOfMetabolites = list(self._DictOfSamples[sample].keys())
            break
        return
    def getListOfMetabolites(self):
        return self._ListOfMetabolites
        
    def getDataFrameOfSamples(self):
        return pd.DataFrame(data=self._DictOfSamples).T
    
    def getConditionAndFeatures(self,FunctionToEvaluateCondition,UsedMetabolites=None):
        x_Data = []
        y_Data = []
        for SampleIdentifiers in self._DictOfSamples:
            
            EvaluatedCondition = FunctionToEvaluateCondition(SampleIdentifiers)
            y_Data.append(EvaluatedCondition)
            SampleProfile = self._DictOfSamples[SampleIdentifiers]
            ListOfSelectedFeatures = []
            for Metabolite in self._ListOfMetabolites:
                if UsedMetabolites == None:
                    ListOfSelectedFeatures.append(SampleProfile[Metabolite])
                elif Metabolite in UsedMetabolites:
                    ListOfSelectedFeatures.append(SampleProfile[Metabolite])
            x_Data.append(ListOfSelectedFeatures)
        return {"x_Data": np.array(x_Data),"y_Data": np.array(y_Data)}
    
    
    def getFold(self,StartStops):
        newFold = MetDataStructure()
        for StartStop in StartStops:
            Start = StartStop[0]
            Stop  = StartStop[1]
            for i in range(Start,Stop):
                SampleCondition = self._ListOfIdentifiers[i]
                SampleMetaboliteProfile = self._DictOfSamples[SampleCondition]
                newFold.addSample(SampleCondition,SampleMetaboliteProfile)
        newFold.upDateMetabolites()
        return newFold
    
    def getNFolds(self,N,Randomize):
        if(Randomize):
            shuffle(self._ListOfIdentifiers)
        
        Shift = int(len(self._ListOfIdentifiers) / N) #Length of Test Data
        NFolds= []
        for i in range (N):
            Extra = 0
            if(i == N -1):
                Extra = len(self._ListOfIdentifiers) % N 
            TrainStartStop =  [[0,i*Shift],[Shift*(i+1),len(self._ListOfIdentifiers) - Extra]]
            TestStartStop   = [[i*Shift,(i+1)*Shift + Extra]]
            NFolds.append([self.getFold(TrainStartStop),self.getFold(TestStartStop)])
        return NFolds
        
    
        