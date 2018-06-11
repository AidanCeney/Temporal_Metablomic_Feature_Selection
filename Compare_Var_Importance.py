import csv
import numpy as np
import ForestCrossVal
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.feature_selection import RFE
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
import Self_Organzing_Map
import pandas as pd


def get_Matching_VarImportance(Top_100_Pimp,Top_100_Vita):
    

    Matches = []
    i = 0
    for Pimp in Top_100_Pimp:
        j = 0
        for Vita in Top_100_Vita:
            if(Pimp[0] == Vita[0] and not Pimp[0] in Matches):
                Matches.append([Pimp[0],i,j])
            j = j+1
        i = i+1
    return Matches
    
def getDataFrameOfVarImp(FileName,Repeat = None):
    Var_Imp = {}
    Flag = True
    with open(FileName, 'rt') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row is not None:
                if Flag:
                    Flag = False
                else:
                    Var_Imp[row[0]] = [float(row[1])]
    DataFrame = pd.DataFrame(data = Var_Imp)
    Name = ""
    if(Repeat == None):
        Name = "VarImp"
    else:
        Name = "VarImp_" + str(Repeat)
    
    DataFrame = DataFrame.rename(index={0: Name})
    return DataFrame.T
    
def get_Top_VarImportance(FileName,nVarImp):
    Var_Imp = []

    with open(FileName, 'rt') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row is not None:
                Var_Imp.append(row)
    del(Var_Imp[0])
    
    
    
    for Samp in Var_Imp:
        Samp[1] = float(Samp[1])
        
   
    
    Top = []
    
    for i in range(len(Var_Imp)):
        
        FlagPIMP = True
        if(i != 0):
            for j in range(len(Top)):
                if(Var_Imp[i][1] > Top[j][1] and FlagPIMP):
                    Top.insert(j,Var_Imp[i])
                    FlagPIMP = False
        if(FlagPIMP):
            Top.append(Var_Imp[i])
        if(len(Top) > nVarImp):
            Top = Top[:nVarImp]
    return Top

def get_Top_VIP_Comp1(FileName,nVarImp):
    Var_Imp = []

    with open(FileName, 'rt') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row is not None:
                Var_Imp.append(row[0:2])
    del(Var_Imp[0])
    

    Top = []
    
    for i in range(len(Var_Imp)):
        
        FlagPIMP = True
        if(i != 0):
            for j in range(len(Top)):
                if(Var_Imp[i][1] > Top[j][1] and FlagPIMP):
                    Top.insert(j,Var_Imp[i])
                    FlagPIMP = False
        if(FlagPIMP):
            Top.append(Var_Imp[i])
        if(len(Top) > nVarImp):
            Top = Top[:nVarImp]
    for Metabo in Top:
        if(Metabo[0][0] != "X"):
            Metabo[0] = "X" + Metabo[0]
    return Top

def get_Top_VIP_Comp2(FileName,nVarImp):
    Var_Imp = []

    with open(FileName, 'rt') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row is not None:
                Var_Imp.append([row[0], row[2]])
    del(Var_Imp[0])
    
    
    
    for Samp in Var_Imp:
        Samp[1] = float(Samp[1])
        
   
    
    Top = []
    
    for i in range(len(Var_Imp)):
        
        FlagPIMP = True
        if(i != 0):
            for j in range(len(Top)):
                if(Var_Imp[i][1] > Top[j][1] and FlagPIMP):
                    Top.insert(j,Var_Imp[i])
                    FlagPIMP = False
        if(FlagPIMP):
            Top.append(Var_Imp[i])
        if(len(Top) > nVarImp):
            Top = Top[:nVarImp]
    return Top
    
def get_Matching_VarImportance(Methode_1,Methode_2,N,Feild):
    rMethode_1 = Methode_1.T.sort_values(by=[Feild],ascending=False).head(N).T
    rMethode_2 = Methode_2.T.sort_values(by=[Feild],ascending=False).head(N).T
    
    ListrMethode_1 = set(list(rMethode_1))
    ListrMethode_2 = set(list(rMethode_2))
    
    return len(ListrMethode_1.intersection(ListrMethode_2))
    
    
    
    
def get_Most_Ref_Metabolite(List_Of_Top_100):
    
    DictOfRanking = {}
    for Top_100 in List_Of_Top_100:
        for Metabo in Top_100:
            if(DictOfRanking.get(Metabo[0]) == None):
                if(type(Top_100[0]) == list):
                    DictOfRanking[Metabo[0]] = {"Total_Ranking": [],"Num_Missed": len(List_Of_Top_100),"Number_Hit": 0, "Avg_Ranking": 0, "STD": 0, "Profile_of_Matches": [0] * len(List_Of_Top_100)}
                else:
                    DictOfRanking[Metabo] = {"Total_Ranking": [],"Num_Missed": len(List_Of_Top_100),"Number_Hit": 0, "Avg_Ranking": 0, "STD": 0, "Profile_of_Matches": [0] * len(List_Of_Top_100)}
                
    for z in range(len(List_Of_Top_100)):
        for i in range(len(List_Of_Top_100[z])):
            Top_100 = List_Of_Top_100[z]
            if(type(Top_100[0]) == list):
                DictOfRanking[Top_100[i][0]]["Total_Ranking"].append(i)
                DictOfRanking[Top_100[i][0]]["Num_Missed"] -= 1
                DictOfRanking[Top_100[i][0]]["Number_Hit"] += 1
                DictOfRanking[Top_100[i][0]]["Profile_of_Matches"][z] = 1
            else:
                DictOfRanking[Top_100[i]]["Total_Ranking"].append(np.nan)
                DictOfRanking[Top_100[i]]["Num_Missed"] -= 1
                DictOfRanking[Top_100[i]]["Number_Hit"] += 1
                DictOfRanking[Top_100[i]]["Profile_of_Matches"][z] = 1
    for Metabo in DictOfRanking:
        DictOfRanking[Metabo]["STD"]         = np.nanstd(np.array(DictOfRanking[Metabo]["Total_Ranking"]))
        DictOfRanking[Metabo]["Avg_Ranking"] = np.nanmean(np.array(DictOfRanking[Metabo]["Total_Ranking"]))
    return DictOfRanking
    

    

def GetMetaboliteNames(DictOfRanking,MetaboliteName):
    
    DictWithNames = {}
    
    for key in DictOfRanking:
        index = int(key[1:])
        DictWithNames[MetaboliteName[index-1]] = DictOfRanking[key]
    return DictWithNames

def Write_Most_Important_Var_in_X_Data(n_VarImp,x_Data,fileName,VIP):
    Top100 = []
    Name = fileName.split(".")[0]
    if(VIP):
        Top100 = get_Top_VIP_Comp1(fileName,n_VarImp)
    else:
        Top100 = get_Top_VarImportance(fileName,n_VarImp)
    x_Data_Most_Imp = []
    for Metabolite in Top100:
        index = int(str(Metabolite[0][1:])) -1
        x_Data_Most_Imp.append(x_Data[index])
    x_Data_Most_Imp = np.transpose(np.array(x_Data_Most_Imp))
    np.savetxt(Name + "_Most_Important_" + str(n_VarImp) +".csv", x_Data_Most_Imp, delimiter =",")
