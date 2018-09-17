import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import CompareMethods
import csv

Class = False
ALL = True

if(ALL):
    Beg = "Res_GC/"
    ListSelected = [Beg + "PLS_Class_Selection.csv",Beg + "PIMP_Class_Selection.csv",Beg + "Vita_Class_Selection.csv"]
    Beg = "Res_Targeted/"
    ListSelected += [Beg + "PLS_Class_Selection.csv",Beg + "PIMP_Class_Selection.csv",Beg + "Vita_Class_Selection.csv"]
    Beg = "Res_LC/"
    ListSelected += [Beg + "PLS_Class_Selection.csv",Beg + "PIMP_Class_Selection.csv",Beg + "Vita_Class_Selection.csv"]
    Beg = "Res_GC/"
    ListSelected += [Beg + "PLS_REG_Selection.csv",Beg + "PIMP_REG_Selection.csv",Beg + "Vita_REG_Selection.csv"]
    Beg = "Res_Targeted/"
    ListSelected += [Beg + "PLS_REG_Selection.csv",Beg + "PIMP_REG_Selection.csv",Beg + "Vita_REG_Selection.csv"]
    Beg = "Res_LC/"
    ListSelected += [Beg + "PLS_REG_Selection.csv",Beg + "PIMP_REG_Selection.csv",Beg + "Vita_REG_Selection.csv"]

elif(Class):
    Beg = "Res_GC/"
    ListSelected = [Beg + "PLS_Class_Selection.csv",Beg + "PIMP_Class_Selection.csv",Beg + "Vita_Class_Selection.csv"]
    Beg = "Res_Targeted/"
    ListSelected += [Beg + "PLS_Class_Selection.csv",Beg + "PIMP_Class_Selection.csv",Beg + "Vita_Class_Selection.csv"]
    Beg = "Res_LC/"
    ListSelected += [Beg + "PLS_Class_Selection.csv",Beg + "PIMP_Class_Selection.csv",Beg + "Vita_Class_Selection.csv"]
else:
    Beg = "Res_GC/"
    ListSelected = [Beg + "PLS_REG_Selection.csv",Beg + "PIMP_REG_Selection.csv",Beg + "Vita_REG_Selection.csv"]
    Beg = "Res_Targeted/"
    ListSelected += [Beg + "PLS_REG_Selection.csv",Beg + "PIMP_REG_Selection.csv",Beg + "Vita_REG_Selection.csv"]
    Beg = "Res_LC/"
    ListSelected += [Beg + "PLS_REG_Selection.csv",Beg + "PIMP_REG_Selection.csv",Beg + "Vita_REG_Selection.csv"]

ListOfMethods = ["R-VIP","R-PIMP","R-Vita"]
ListOfMethods = ListOfMethods + ListOfMethods + ListOfMethods
if(ALL):
    ListOfMethods2 = ["C-VIP","C-PIMP","C-Vita"]
    ListOfMethods += ListOfMethods2 + ListOfMethods2 + ListOfMethods2

DFOverLap = CompareMethods.getMethodeOverlap(ListSelected,ListOfMethods).T.sort_values(by=["NumSelected"],ascending=False)

if(ALL):
    DFOverLap.to_csv(path_or_buf="OverLap_Res/AllDF.csv")
elif(Class):
    DFOverLap.to_csv(path_or_buf="OverLap_Res/ClassDF.csv")
else:
    DFOverLap.to_csv(path_or_buf="OverLap_Res/RegDF.csv")
OverLap = CompareMethods.getNumMethodeOverlap(DFOverLap.T)


with open("lstRFE.csv", 'w') as myfile:
    wr = csv.writer(myfile, )
    wr.writerow(OverLap["RFE"])
with open("lstVIP.csv", 'w') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(OverLap["VIP"])
with open("lstPIMP.csv", 'w') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(OverLap["PIMP"])
with open("lstVita.csv", 'w') as myfile:
    wr = csv.writer(myfile)
    wr.writerow(OverLap["Vita"])