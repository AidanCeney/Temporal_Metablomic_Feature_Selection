import subprocess
import os
import csv
import pandas as pd


def RFVita():
    Argument = [os.getcwd() +'/RFVitaNImportant.R', '/TmpFiles/x_Data_Train_' + str(os.getpid()) + '.csv','/TmpFiles/y_Data_Train_' + str(os.getpid()) +'.csv','/TmpFiles/VitaNSelected' +       str(os.getpid()) +'.csv']
    process = subprocess.Popen(Argument,stderr=subprocess.PIPE)
    process.wait()
    return
def RFPIMP():
    Argument = [os.getcwd() +'/RFPIMPNImportant.R', '/TmpFiles/x_Data_Train_' + str(os.getpid()) + '.csv','/TmpFiles/y_Data_Train_' + str(os.getpid()) +'.csv','/TmpFiles/PimpNSelected' +       str(os.getpid()) +'.csv']
    process = subprocess.Popen(Argument,stderr=subprocess.PIPE)
    process.wait()
    return
def PLSVIP():
    Argument = [os.getcwd() +'/PLSNImportant.R', '/TmpFiles/x_Data_Train_' + str(os.getpid()) +'.csv','/TmpFiles/y_Data_Train_' + str(os.getpid()) +'.csv','/TmpFiles/PLSNSelected' +       str(os.getpid()) +'.csv']
    process = subprocess.Popen(Argument,stderr=subprocess.PIPE)
    process.wait()
    return  
def TestRF():
    args = [os.getcwd() + '/CheckRf.R','/Fold/x_Data_Train_' + str(os.getpid()) + '.csv','/Fold/y_Data_Train_' + str(os.getpid()) + '.csv','/Fold/x_Data_Test_' + str(os.getpid()) + '.csv',"/Fold/y_Test_Res_RF_" + str(os.getpid()) + ".csv"]
    process = subprocess.Popen(args,stderr=subprocess.PIPE)
    process.wait()
    return
def TestPLS():
    process = subprocess.Popen([os.getcwd() + '/CheckPLS.R','/Fold/x_Data_Train_' + str(os.getpid()) + '.csv','/Fold/y_Data_Train_' + str(os.getpid()) + '.csv','/Fold/x_Data_Test_' + str(os.getpid()) + '.csv',"/Fold/y_Test_Res_PLS_" + str(os.getpid()) + ".csv"],stderr=subprocess.PIPE)
    process.wait()
    return

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
def ConvertListOfDictsToDictOfLists(LOD):
    DOL = {}
    for aKey in LOD[0]:
        DOL[aKey] = []
    for items in LOD:
        for aKey in items:
            DOL[aKey].append(items[aKey])
    return DOL

def calcPLSdaRes(ResPLSDADataFrame):
    
    Results = ResPLSDADataFrame["X0.dim.1"].values + ResPLSDADataFrame["X0.dim.2"].values
    
    return [int(res <= 1)for res in Results]