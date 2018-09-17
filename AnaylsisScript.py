import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import pylab
from matplotlib.pyplot import figure

Beg = "Res_Targeted/"


SVMREG   = pd.read_csv(Beg + "SVM_REG_Fitness.csv", index_col = 0)
SVMClass = pd.read_csv(Beg + "SVM_Class_Fitness.csv", index_col = 0)
TestSVMREG   = pd.read_csv(Beg + "Test_SVM_REG_Fitness.csv", index_col = 0)
TestSVMClass = pd.read_csv(Beg + "Test_SVM_Class_Fitness.csv", index_col = 0)

VitaREG = pd.read_csv(Beg + "Vita_REG_Fitness.csv", index_col = 0)
VitaClass = pd.read_csv(Beg + "Vita_Class_Fitness.csv", index_col = 0)

PIMPREG = pd.read_csv(Beg + "PIMP_REG_Fitness.csv", index_col = 0)

TestRFREG = pd.read_csv(Beg + "Test_RF_REG_Fitness.csv", index_col = 0)
TestRF = pd.read_csv(Beg + "Test_RF_Class_Fitness.csv", index_col = 0)

PLSREG       = pd.read_csv(Beg + "PLS_REG_Fitness.csv",   index_col = 0)
PLSClass     = pd.read_csv(Beg + "PLS_CLass_Fitness.csv", index_col = 0)
TestPLSREG   = pd.read_csv(Beg + "Test_PLS_REG_Fitness.csv",   index_col = 0)
TestPLSClass = pd.read_csv(Beg + "Test_PLS_CLass_Fitness.csv", index_col = 0)

a = [SVMREG["RMSE"].Mean,VitaREG["RMSE"].Mean,PIMPREG["RMSE"].Mean,PLSREG["RMSE"].Mean,TestSVMREG["RMSE"].Mean,TestRFREG["RMSE"].Mean,TestPLSREG["RMSE"].Mean]
b = [SVMREG["Qsqd"].Mean,VitaREG["Qsqd"].Mean,PIMPREG["Qsqd"].Mean,PLSREG["Qsqd"].Mean,TestSVMREG["Qsqd"].Mean,TestRFREG["Qsqd"].Mean,TestPLSREG["Qsqd"].Mean]
c = [SVMREG["RMSE"].STD,VitaREG["RMSE"].STD,PIMPREG["RMSE"].STD,PLSREG["RMSE"].STD,TestSVMREG["RMSE"].STD,TestRFREG["RMSE"].STD,TestPLSREG["RMSE"].STD]
d = [SVMREG["Qsqd"].STD,VitaREG["Qsqd"].STD,PIMPREG["Qsqd"].STD,PLSREG["Qsqd"].STD,TestSVMREG["Qsqd"].STD,TestRFREG["Qsqd"].STD,TestPLSREG["Qsqd"].STD]

name = ['SVM-RFE','RF-Vita','RF-PIMP','PLS-VIP','SVM-ALL','RF-ALL','PLS-ALL']
colors=['c', 'b', 'gold', 'm', 'r','seagreen','brown']

figure(num=None, figsize=(10, 6), dpi=80, facecolor='w', edgecolor='k')

for i in range(len(a)):
    plt.errorbar(a[i],b[i],xerr=c[i],yerr=d[i],capsize=2,fmt="none",color=colors[i],linewidth = .25)
    plt.scatter(a[i],b[i],label=name[i],color=colors[i])



plt.xlabel("RMSE",fontsize=12)
plt.ylabel("$Q^{2}$",fontsize=12)


plt.show()

