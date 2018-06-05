import csv
import numpy as np




def readMetaboliteAndCondition(MetaboliteFiles):
    
    ListMetaboliteNames = []
    MetaboliteData = {}
    
    for FileName in MetaboliteFiles:
        Raw_Data = []
        with open(FileName, 'rt') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row is not None:
                    Raw_Data.append(row)
        
        
        UnNeededRow = ['order','number','MST','time','rep',]
        numToElimnatePast = 1
        for name in Raw_Data[0][0:10]:
            if(name in UnNeededRow):
                numToElimnatePast += 1
        MetaboliteNames = Raw_Data[0][1+numToElimnatePast:]
        MetaboliteNames = list(map(lambda x: addFilePrefix(x,FileName.split("/")[1]),MetaboliteNames))
        MetaboliteNames = ChangeDuplicates(MetaboliteNames)
        ListMetaboliteNames = ListMetaboliteNames + MetaboliteNames
        del Raw_Data[0]
        count = 0
        
        for Samp in Raw_Data:
            
            del Samp[0]
            Name = Samp[0]
            for i in range(numToElimnatePast):
                del Samp[0]
            broken = Name.split('-')
            
            if(broken[0] == "QC"):
                continue
            SampNumber = broken[0]
            if(type(MetaboliteData.get(SampNumber)) != np.ndarray):
                MetaboliteData[SampNumber] = np.array(list(map(convertToFloat,Samp)))
            else:
                MetaboliteData[SampNumber] =  np.append(MetaboliteData[SampNumber], np.array(list(map(convertToFloat,Samp))))
      
        
        del(Raw_Data)
    
    
        
    yTemplate = {1 : 0, 2 : 1, 3 : 1.5, 4 : 2, 5 : 2.5, 6 : 3, 7 : 4, 8 : 6, 9 : 8, 10 : 10, 11 : 12, 12 : 13, 13 : 13.5, 14 : 14, 15 : 14.5, 16 : 15,17 : 16, 18 : 18, 19 : 20, 20 : 22, 21 : 24, 22 : 25, 23 : 25.5, 24 : 26} 
        
    y_Data = []
    y_ClassData = []
    x_Data = np.array(list(MetaboliteData.values()))
    for SampNumber  in MetaboliteData:
        key = int((int(SampNumber)-1)/3) + 1
        y_Data.append(yTemplate[key])
        y_ClassData.append(1 if 13 <= int(SampNumber) <= 39 else 0) #Sets y_classification to On for samples 13-39 and off for remaining samples
        
        
    y_ClassData = np.array(list(map(int,y_ClassData)))
    y_Data = np.array(y_Data)
    Removed  = RemoveMetabolitesWithNAN(x_Data,ListMetaboliteNames)
    x_Data = Removed[0]
    ListMetaboliteNames = Removed[1]
    ListMetaboliteNames = FixNa(ListMetaboliteNames)
    
    return [x_Data,y_Data,y_ClassData,ListMetaboliteNames]

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

def getParetoScale(FileName):
    
    MetaboliteData = []
    Raw_Data = []
    with open(FileName, 'rt') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row is not None:
                Raw_Data.append(row)
    del[Raw_Data[0]]
    for Samp in Raw_Data:
        del Samp[0]
        MetaboliteData.append(np.array(list(map(convertToFloat,Samp))))
    
    return np.array(MetaboliteData)
    
    

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

def convertToFloat(astr):
    if astr == "NA":
        return np.NaN
    else: 
        return float(astr)
def RemoveMetabolitesWithNAN(Metabolites,MetaboliteNames):
    tMetabolites = np.transpose(Metabolites)
    count = 0
    for i in range(len(tMetabolites)):
        if sum(np.isnan(tMetabolites[i])) != 0:
            Metabolites = np.delete(Metabolites,i,axis = 1)
            del(MetaboliteNames[i])
            count = count + 1
    print("Num Removed: " + str(count))
    return [Metabolites, MetaboliteNames]