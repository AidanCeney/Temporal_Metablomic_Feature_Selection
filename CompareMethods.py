import numpy as np
import ForestCrossVal
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.svm import SVC
from sklearn.feature_selection import RFE
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
from scipy.stats import pareto
import Self_Organzing_Map
from sklearn.cluster import AgglomerativeClustering
import HClusterAnaylsis
import Compare_Var_Importance
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import ResAnaylsis
import MetFileParser
import os
import subprocess
import stat
import copy


def getResultsRF(FileList,Num,NVar):
    
    Data =  MetFileParser.readMetaboliteAndCondition(FileList)
    x_Data = Data[0]
    y_Data = Data[1]
    y_Data_Class = Data[2]
    Metabolite_Names = Data[3]
    
    np.savetxt('x_Data.csv',x_Data,delimiter =",")
    np.savetxt('y_Data.csv',y_Data,delimiter =",")
    np.savetxt('y_Data_class.csv',y_Data_Class,delimiter =",")
    
    RF()
    

    DictOfImportantVar = getAllRFNImportant(Num)
    ParetoComp = getParetoComparison(DictOfImportantVar,Num,NVar)
    
    DictofResults = {"DictOfImportantVar": DictOfImportantVar,"ParetoComp": ParetoComp}
    
    return DictofResults 
    
def RF():
    process = subprocess.Popen(os.getcwd() +'/RegresionForest.R',stderr=subprocess.PIPE)
    process.wait()
    return
def PLS():
     
    process = subprocess.Popen((os.getcwd() + '/PLSAnaylsis.R'),stderr=subprocess.PIPE)
    process.wait()
    return  

def TestRF(addArgs):
    args = [os.getcwd() +'/CheckRF.R']
    args.extend(addArgs)
    process = subprocess.Popen(args,stderr=subprocess.PIPE)
    process.wait()
    return
def TestPLS(addArgs):
    args = [os.getcwd() +'/CheckPLS.R']
    args.extend(addArgs)
    process = subprocess.Popen(args,stderr=subprocess.PIPE)
    process.wait()
    return  

def getAllRFNImportant(Num):
    
    
    DictOfImportantVar = {}
    

        
    DictOfImportantVar["None_Pimp_Regresion"]        = Compare_Var_Importance.getDataFrameOfVarImp('Reasources/Pimp_Var_Importance.csv',Num)
    DictOfImportantVar["None_Vita_Regresion"]        = Compare_Var_Importance.getDataFrameOfVarImp('Reasources/Vita_Var_Importance.csv',Num)
    DictOfImportantVar["Pareto_Pimp__Regresion"]     = Compare_Var_Importance.getDataFrameOfVarImp('Reasources/Pareto_Pimp_Var_Importance.csv',Num)
    DictOfImportantVar["Pareto_Vita__Regresion"]     = Compare_Var_Importance.getDataFrameOfVarImp('Reasources/Pareto_Vita_Var_Importance.csv',Num)
    
    DictOfImportantVar["None_Pimp_Class"]        = Compare_Var_Importance.getDataFrameOfVarImp('Reasources/Pimp_Var_Importance_Class.csv',Num)
    DictOfImportantVar["None_Vita_Class"]        = Compare_Var_Importance.getDataFrameOfVarImp('Reasources/Vita_Var_Importance_Class.csv',Num)
    DictOfImportantVar["Pareto_Pimp_Class"]      = Compare_Var_Importance.getDataFrameOfVarImp('Reasources/Pareto_Pimp_Var_Importance_Class.csv',Num)
    DictOfImportantVar["Pareto_Vita_Class"]      = Compare_Var_Importance.getDataFrameOfVarImp('Reasources/Pareto_Vita_Var_Importance_Class.csv',Num)
    

    
    return DictOfImportantVar
    
def getAllPLSNImportant():
    
    
    DictOfImportantVar = {}
    
    DictOfImportantVar["None_PLS_Comp1"]            = Compare_Var_Importance.getDataFrameOfVarImp("Reasources/PLS_VIP.csv")
    DictOfImportantVar["Pareto_PLS_Comp1"]          = Compare_Var_Importance.getDataFrameOfVarImp("Reasources/Pareto_PLS_VIP.csv")
    DictOfImportantVar["None_PLSDA_Comp1"]          = Compare_Var_Importance.getDataFrameOfVarImp("Reasources/PLS-DA_VIP.csv")
    DictOfImportantVar["Pareto_PLSDA_Comp1"]        = Compare_Var_Importance.getDataFrameOfVarImp("Reasources/Pareto_PLS-DA_VIP.csv")
    
    
    return DictOfImportantVar
    
def getALLKernSVM(x_Data,y_Data,y_Data_Class,N):
    DictOfImportantVar = {}
    DictOfImportantVar["Pareto_SVM_REG"]        = getSVMResults(x_Data,y_Data,N,Scaling = "Pareto",Mode = "Regression")
    DictOfImportantVar["None_SVM_REG"]          = getSVMResults(x_Data,y_Data,N,Scaling = "None",  Mode = "Regression")
    DictOfImportantVar["Pareto_SVM_Class"]      = getSVMResults(x_Data,y_Data_Class,N,Scaling = "Pareto",Mode = "Class")
    DictOfImportantVar["None_SVM_Class"]        = getSVMResults(x_Data,y_Data_Class,N,Scaling = "None",Mode = "Class")
    
    return DictOfImportantVar
    
    
    
def getParetoComparison(DictOfImportantVar,Num,NVar):
  
    Pairings = {}
    for Name in DictOfImportantVar:
        
        Identifiers = Name.split("_")
        Mode = "".join(Identifiers[1:])
        if(Pairings.get(Mode) == None):
            Pairings[Mode] = {Identifiers[0]: DictOfImportantVar[Name]}
        else:
            Pairings[Mode][Identifiers[0]] = DictOfImportantVar[Name]
    
    NumberOfMatching = {}
    
    for Pair in Pairings:
        NumberOfMatching[Pair + "_" + str(Num)] = Compare_Var_Importance.get_Matching_VarImportance(Pairings[Pair]["Pareto"].T,Pairings[Pair]["None"].T,NVar,"VarImp_" + str(Num))
    
    return NumberOfMatching
    

def getRepeatedResults(FileList,N,Number):
    
    Data =  MetFileParser.readMetaboliteAndCondition(FileList)
    x_Data = Data[0]
    y_Data = Data[1]
    y_Data_Class = Data[2]
    Metabolite_Names = Data[3]
    
    
    
    RepeatedDictOfImportantVarRF = []
    RepeatedParetoCompRF = []
    Res = {}
    
    
    for i in range(Number):
        Res = getResultsRF(FileList,i,N)
        RepeatedDictOfImportantVarRF.append(Res["DictOfImportantVar"])
        RepeatedParetoCompRF.append(Res["ParetoComp"])
    
    PLS()
    PLSRes = CombineResultsNImp([getAllPLSNImportant()],N)
    SVMRes = getALLKernSVM(x_Data,y_Data,y_Data_Class,N)
    
    RepeatedDictOfImportantVarRF = CombineResultsNImp(RepeatedDictOfImportantVarRF,N)
    
    RepeatedDictOfImportantVar = {**RepeatedDictOfImportantVarRF, **PLSRes, **SVMRes}
    
    ChangeName(RepeatedDictOfImportantVar,Metabolite_Names)
    
    RepeatedParetoComp = getParetoOverlap(RepeatedDictOfImportantVar) 
    RepeatedDictOfImportantVarOverlap = getMethodeOverlap(RepeatedDictOfImportantVar,True)
    
    
    DictofResults = {"RepeatedDictOfImportantVar": RepeatedDictOfImportantVar,"RepeatedDictOfImportantVarOverlap": RepeatedDictOfImportantVarOverlap,"RepeatedParetoComp": RepeatedParetoComp,"x_Data": x_Data,"y_Data": y_Data,"y_Data_Class": y_Data_Class, "Metabolite_Names": Metabolite_Names}
    
    return DictofResults
    

    
def getParetoOverlap(RepeatedDictOfImportantVar):
    ParetoMatching = {}
    for Methode in RepeatedDictOfImportantVar:
        Name = "".join(Methode.split("_")[1:])
        if ParetoMatching.get(Name) is None:
            if type(RepeatedDictOfImportantVar[Methode]) is pd.DataFrame:
                ParetoMatching[Name] = set(RepeatedDictOfImportantVar[Methode].index.values)
            else:
                ParetoMatching[Name] = set(RepeatedDictOfImportantVar[Methode])
        else:
            if type(RepeatedDictOfImportantVar[Methode]) is pd.DataFrame:
                ParetoMatching[Name] = len(ParetoMatching[Name].intersection(set(RepeatedDictOfImportantVar[Methode].index.values)))
            else:
                ParetoMatching[Name] = len(ParetoMatching[Name].intersection(set(RepeatedDictOfImportantVar[Methode])))
    return ParetoMatching

def getMethodeOverlap(RepeatedDictOfImportantVar,Pareto):
    
    RepeatedDictOfImportantVar = copy.deepcopy(RepeatedDictOfImportantVar)
    
    for keys in list(RepeatedDictOfImportantVar.keys()):
        Scaling = keys.split("_")[0]
        if(Pareto and Scaling != "Pareto"):
            del(RepeatedDictOfImportantVar[keys])
        elif(not Pareto and Scaling != "None"):
            del(RepeatedDictOfImportantVar[keys])
            
    
    DictOfOverlap = {}
    for Methode in RepeatedDictOfImportantVar:
        if(type(RepeatedDictOfImportantVar[Methode]) is pd.DataFrame):
            for Metabolite in list(RepeatedDictOfImportantVar[Methode].T.columns.values):
                if(DictOfOverlap.get(Metabolite) == None):
                    DictOfOverlap[Metabolite] = {"Total_Ranking": [],"Num_Missed": len(RepeatedDictOfImportantVar),"Number_Hit": 0, "Avg_Ranking": 0, "STD": 0, "Profile_of_Matches": [] }
                    
        elif(type(RepeatedDictOfImportantVar[Methode]) is list):
             for Metabolite in RepeatedDictOfImportantVar[Methode]:
                if(DictOfOverlap.get(Metabolite) == None):
                    DictOfOverlap[Metabolite] = {"Total_Ranking": [],"Num_Missed": len(RepeatedDictOfImportantVar),"Number_Hit": 0, "Avg_Ranking": 0, "STD": 0, "Profile_of_Matches": []}
    
    for Methode in RepeatedDictOfImportantVar:
        SplitMeth = Methode.split("_")
        if(type(RepeatedDictOfImportantVar[Methode]) is pd.DataFrame):
            for index, row in RepeatedDictOfImportantVar[Methode].iterrows():
                DictOfOverlap[index]["Total_Ranking"].append(row["Rel_Imp"])
                DictOfOverlap[index]["Num_Missed"] -= 1
                DictOfOverlap[index]["Number_Hit"] += 1
                DictOfOverlap[index]["Profile_of_Matches"].append(SplitMeth[1] + SplitMeth[2])
        
        if(type(RepeatedDictOfImportantVar[Methode]) is list):
            for index in RepeatedDictOfImportantVar[Methode]:
                DictOfOverlap[index]["Total_Ranking"].append(np.NaN)
                DictOfOverlap[index]["Num_Missed"] -= 1
                DictOfOverlap[index]["Number_Hit"] += 1
                DictOfOverlap[index]["Profile_of_Matches"].append(SplitMeth[1] + SplitMeth[2]) 
    for Metabo in DictOfOverlap:
        DictOfOverlap[Metabo]["Total_Ranking"] = np.array(DictOfOverlap[Metabo]["Total_Ranking"])
        DictOfOverlap[Metabo]["Avg_Ranking"] = np.nanmean(DictOfOverlap[Metabo]["Total_Ranking"])
        DictOfOverlap[Metabo]["STD"] = np.nanstd(DictOfOverlap[Metabo]["Total_Ranking"])
    
    return pd.DataFrame(data = DictOfOverlap).T
    
def CombineResultsNImp(ListOfResults,N):
    
    DictofMethods = {}
    for Results in ListOfResults:
        for Methode in Results:
            if(type(DictofMethods.get(Methode)) is not pd.DataFrame):
                DictofMethods[Methode] = Results[Methode]
            else:
                DictofMethods[Methode] = pd.concat([DictofMethods[Methode], Results[Methode]],axis = 1) 
    RetResults = {}
    
    
    for Methode in DictofMethods:
        RetResults[Methode] = pd.DataFrame(data = {"VarImp": DictofMethods[Methode].T.mean(), "STD": DictofMethods[Methode].T.std()}).sort_values(by=["VarImp"],ascending=False).head(N)
        RetResults[Methode]["Rel_Imp"] = pd.Series(range(N), index=RetResults[Methode].index)
    
    return RetResults
    
def plotMethodeOverlap(MetaboliteProfile,NumMatching):
    MetaboliteProfile = MetaboliteProfile[MetaboliteProfile.Number_Hit >= 4]
    DictOfOverlap = {}
    for index, row in MetaboliteProfile.iterrows():
        for Methode in row["Profile_of_Matches"]:
            if(DictOfOverlap.get(Methode) == None):
                DictOfOverlap[Methode] = {"Number of Matches": 1,"Methode": Methode}
            
            else:
                DictOfOverlap[Methode]["Number of Matches"] += 1
    DataFrameOfMatches = pd.DataFrame(data = DictOfOverlap)
    g = sns.factorplot(x="Methode", y="Number of Matches", data=DataFrameOfMatches.T, saturation=.5, kind="bar", ci=None, aspect=1.5)
    plt.title("Number of Methode Overlap")
    plt.show()
    return
    
        
        
    

def getSVMResults(x_Data,y_Data,N,Scaling = "Pareto",Mode = "Class"):
    
    if(Scaling == "Pareto"):
        x_Data = MetFileParser.ParetoScale(x_Data)
    
    if (Mode == "Class"):
        Class_SVM = SVC(kernel="linear")
        Class_RFE = RFE(Class_SVM, N, step=10)
        Class_RFE = Class_RFE.fit(x_Data,y_Data)
        
        Top100_Class = []
        for i in range(len(Class_RFE.ranking_)):
            if(Class_RFE.ranking_[i] == 1):
                Top100_Class.append("X"+ str(i + 1))
        return Top100_Class
    
    elif (Mode == "Regression"):
          REG_SVM   = SVR(kernel="linear")
          REG_RFE   = RFE(REG_SVM, N, step=10)   
          REG_RFE   = REG_RFE.fit(x_Data,y_Data)
    
          Top100_REG = []
          for i in range(len(REG_RFE.ranking_)):
            if(REG_RFE.ranking_[i] == 1):
                Top100_REG.append("X"+ str(i + 1))
          return Top100_REG
    return -1
    
def ChangeName(RepeatedDictOfImportantVar,ListOfNames):
    for Methode in RepeatedDictOfImportantVar:
        if(type(RepeatedDictOfImportantVar[Methode]) is pd.DataFrame or pd.Series):
            NewIndexs = []
            for index in RepeatedDictOfImportantVar[Methode].index.tolist():
                NewIndexs.append(ListOfNames[int(index[1:])-1])
            RepeatedDictOfImportantVar[Methode].index = NewIndexs
        elif(type(RepeatedDictOfImportantVar[Methode]) is  list):
            NewIndexs = []
            for item in RepeatedDictOfImportantVar[Methode]:
                NewIndexs.append(ListOfNames[int(item[1:])-1])
            RepeatedDictOfImportantVar[Methode] = NewIndexs
    return
def ChangeIndName(StructureOfNames,ListOfNames):
    if(type(StructureOfNames) is pd.DataFrame or pd.Series):
        NewIndexs = []
        for index in StructureOfNames.index.tolist():
            NewIndexs.append(ListOfNames[int(index[1:])-1])
        StructureOfNames.index = NewIndexs
    elif(type(StructureOfNames) is  list):
        NewIndexs = []
        for item in StructureOfNames:
            NewIndexs.append(ListOfNames[int(item[1:])-1])
        StructureOfNames = NewIndexs
    return

def TestAcuaracy(ListOfUsedMetabolites,ListOfMetaboliteNames,x_Data,y_Data,numFolds,Mode = "All",N=1,RUN_NAME = ""):
    x_Data = np.transpose(getUsed(ListOfUsedMetabolites,ListOfMetaboliteNames,x_Data))
    Class = max(y_Data) == 1
    doSVM = True
    doRF  = True
    doPLS = True
    
    if(Mode != "All"):
        doSVM = Mode == "SVM" 
        doRF  = Mode == "RF" 
        doPLS = Mode == "PLS" 
    
    Res = {}
   
    
    for j in range(N):
        rSample = ForestCrossVal.RandomizeSample(x_Data, y_Data)
        x_Data = rSample[0]
        y_Data = rSample[1]
        Folds = ForestCrossVal.CrossVal(x_Data, y_Data,numFolds)
        
        X_Trains = Folds[0]
        Y_Trains = Folds[1]
        X_Test = Folds[2]
        Y_Test = Folds[3]
        
        for i in range(numFolds):
            cX_Train = X_Trains[i]
            cY_Train = Y_Trains[i]
            
            cX_Test = X_Test[i]
            cY_Test = Y_Test[i]
            
            np.savetxt('Fold/x_Data_Train_' + str(os.getpid()) +'.csv',cX_Train,delimiter =",")
            np.savetxt('Fold/y_Data_Train_' + str(os.getpid()) +'.csv',cY_Train,delimiter =",")
            
            np.savetxt('Fold/x_Data_Test_' + str(os.getpid()) +'.csv',cX_Test,delimiter =",")
            
            
            if(doPLS):
                TestPLS(['/Fold/x_Data_Train_' + str(os.getpid()) + '.csv','/Fold/y_Data_Train_' + str(os.getpid()) + '.csv','/Fold/x_Data_Test_' + str(os.getpid()) + '.csv',"/Fold/y_Test_Res_PLS_" + str(os.getpid()) + ".csv"])
                PLSRes = pd.read_csv("Fold/y_Test_Res_PLS_" + str(os.getpid()) + ".csv",index_col = 0)
            
                
                if(Class):
                    PLSRes = calcPLSdaRes(PLSRes)
                    Res["PLS"+RUN_NAME+"_RUN_"+str(j)+"Fold_"+str(i)] = {"True_Negative" : ResAnaylsis.getFalsePositiveRate(PLSRes,cY_Test),"True_Positive": ResAnaylsis.getTruePositiveRate(PLSRes,cY_Test), "Mode": "PLS"+RUN_NAME} 
    
                else:
                    PLSRes = list(PLSRes.mean(1).values)
                    Res["PLS"+RUN_NAME+"_RUN_"+str(j)+"Fold_"+str(i)] = {"RMSE": ResAnaylsis.getRMSE(PLSRes,cY_Test), "Mode": "PLS"+RUN_NAME} 
                
            if(doRF):
                TestRF(['/Fold/x_Data_Train_' + str(os.getpid()) + '.csv','/Fold/y_Data_Train_' + str(os.getpid()) + '.csv','/Fold/x_Data_Test_' + str(os.getpid()) + '.csv',"/Fold/y_Test_Res_RF_" + str(os.getpid()) + ".csv"])
                RFRes  = pd.read_csv("Fold/y_Test_Res_RF_"+ str(os.getpid()) +".csv", index_col = 0)
                RFRes = list(RFRes.mean(1).values)
                
                if(Class):
                    Res["RF"+RUN_NAME+"_RUN_"+str(j)+"Fold_"+str(i)] = {"True_Negative" : ResAnaylsis.getFalsePositiveRate(RFRes,cY_Test),"True_Positive": ResAnaylsis.getTruePositiveRate(RFRes,cY_Test), "Mode": "RF"+RUN_NAME} 
                else:
                    Res["RF"+RUN_NAME+"_RUN_"+str(j)+"Fold_"+str(i)] = {"RMSE": ResAnaylsis.getRMSE(RFRes,cY_Test), "Mode": "RF"+RUN_NAME} 
                   
            if(doSVM):
                
                if(Class):
                    Class_SVM = SVC(kernel="linear").fit(MetFileParser.ParetoScale(cX_Train),cY_Train)
            
                    SVMRes = Class_SVM.predict(cX_Test)
                    Res["SVM"+RUN_NAME+"_RUN_"+str(j)+"Fold_"+str(i)] = {"True_Negative" : ResAnaylsis.getFalsePositiveRate(SVMRes,cY_Test),"True_Positive": ResAnaylsis.getTruePositiveRate(SVMRes,cY_Test),"Mode": "SVM" + RUN_NAME} 
                else:
                    REG_SVM = SVR(kernel="linear").fit(MetFileParser.ParetoScale(cX_Train),cY_Train)
                
                    SVMRes = REG_SVM.predict(cX_Test)
                    Res["SVM"+RUN_NAME+"_RUN_"+str(j)+"Fold_"+str(i)] = {"RMSE": ResAnaylsis.getRMSE(SVMRes,cY_Test), "Mode": "SVM"+RUN_NAME}
                    
    os.remove('Fold/x_Data_Train_' + str(os.getpid()) +'.csv')
    os.remove('Fold/y_Data_Train_' + str(os.getpid()) +'.csv')
    os.remove('Fold/x_Data_Test_' + str(os.getpid()) +'.csv')
    if(doPLS):
        os.remove("Fold/y_Test_Res_PLS_" + str(os.getpid()) + ".csv",cX_Test,delimiter =",")
    if(doRF):
        os.remove("Fold/y_Test_Res_RF_"+ str(os.getpid()) +".csv")
    
    return Res
      

def getUsed(ListOfUsedMetabolites,ListOfMetaboliteNames,x_Data):
    
   
    UsedArray = []
    for Metabo in ListOfUsedMetabolites:
        index = ListOfMetaboliteNames.index(Metabo)
        UsedArray.append(x_Data[:,index])
    return np.array(UsedArray)

def calcPLSdaRes(ResPLSDADataFrame):
    
    Results = ResPLSDADataFrame["X0.dim.1"].values + ResPLSDADataFrame["X0.dim.2"].values
    
    return [int(res <= 1)for res in Results]

def getUsedFeatures(GenomeOfFeatures,NameOfFeatures):
    
    usedFeatures = []
    for i in range(len(GenomeOfFeatures)):
        if(GenomeOfFeatures[i]):
            usedFeatures.append(NameOfFeatures[i])
    return usedFeatures
    
    

def FitnessPLSRMSE(FeatureProfile,ListOfMetaboliteNames,x_Data,y_Data,numFolds):
    PLSResults = TestAcuaracy(getUsedFeatures(FeatureProfile,ListOfMetaboliteNames),ListOfMetaboliteNames,x_Data,y_Data,numFolds,Mode = "PLS",N=3,RUN_NAME = "PLS_Test")
    PLSResults = pd.DataFrame(data = PLSResults).T
    Fitness    = 1 / PLSResults["RMSE"].mean()
    return Fitness

def FitnessRFRMSE(FeatureProfile,ListOfMetaboliteNames,x_Data,y_Data,numFolds):
    RFResults = TestAcuaracy(getUsedFeatures(FeatureProfile,ListOfMetaboliteNames),ListOfMetaboliteNames,x_Data,y_Data,numFolds,Mode = "RF",N=3,RUN_NAME = "PLS_Test")
    RFResults = pd.DataFrame(data = RFResults).T
    Fitness    = 1 / RFResults["RMSE"].mean()
    return Fitness


'''
    
    
   
'''


    
