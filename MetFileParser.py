import csv
import numpy as np
import MetablomicsDataStructure
import SelectFeatures



def readMetaboliteAndCondition(MetaboliteFiles,IdentifierColumnIndexs,IgnoredColumnIndexs,UsedSamples):
    
    MetaboliteData = {}
    MetablomicsData = MetablomicsDataStructure.MetDataStructure()
    Count = 0
    for FileName in MetaboliteFiles:
        Raw_Data = []
        with open(FileName, 'rt') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row is not None:
                    Raw_Data.append(row)
      
        MetaboliteNames = Raw_Data[0]
        MetaboliteNames = list(map(lambda x: addFilePrefix(x,FileName.split("/")[1]),MetaboliteNames))
        MetaboliteNames = ChangeDuplicates(MetaboliteNames)
        del Raw_Data[0]
        index = 0
        for Samp in Raw_Data:
            if(index not in UsedSamples):
                index += 1
                continue
            index += 1
            NumDel = 0
            SampleMetaboliteProfile = {}
            Identifier = ""
            for i in range(len(Samp)):
                if (i == IdentifierColumnIndexs[Count]):
                    Identifier = Samp[i]
                elif(i not in IgnoredColumnIndexs[Count]):
                    SampleMetaboliteProfile[MetaboliteNames[i]] = float(Samp[i])
            MetablomicsData.addSample(Identifier,SampleMetaboliteProfile)
        Count += 1  
    MetablomicsData.upDateMetabolites()  
    return MetablomicsData

def FixNa(NList):
    count = 0
    NewNList = []
    for item in NList:
        Name = item.split("_")[1]
        if(Name == "NA"):
            NewNList.append(item + "_" + str(count))
            count += 1
        else:
            NewNList.append(item)
    return NewNList

def ParetoScale(Data):
    tMetabolites = np.transpose(Data)
    for MetaboProfile in tMetabolites:
        Mean = np.mean(MetaboProfile)
        STD = np.std(MetaboProfile)
        MetaboProfile = (MetaboProfile - Mean) / np.sqrt(STD)
    return np.transpose(tMetabolites)

def addFilePrefix(MetName,FileName):
    return FileName[0:2] + "_" + MetName

def ChangeDuplicates(MetName):
    Dup = {}
    Result = []
    for name in MetName:
        if(Dup.get(name) == None):
            Dup[name] = 1
            Result.append(name)
        else:
            Dup[name] += 1
            Result.append(name + "_" +str(Dup[name]))
    return Result
