import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import pylab
from matplotlib.pyplot import figure
Beg = "Res_Targeted/"


SVMClass = pd.read_csv(Beg + "SVM_Class_Fitness.csv", index_col = 0)
TestSVMClass = pd.read_csv(Beg + "Test_SVM_Class_Fitness.csv", index_col = 0)


VitaClass = pd.read_csv(Beg + "Vita_Class_Fitness.csv", index_col = 0)

PIMClass = pd.read_csv(Beg + "PIMP_Class_Fitness.csv", index_col = 0)


TestRFClass = pd.read_csv(Beg + "Test_RF_Class_Fitness.csv", index_col = 0)


PLSClass     = pd.read_csv(Beg + "PLS_CLass_Fitness.csv", index_col = 0)
TestPLSClass = pd.read_csv(Beg + "Test_PLS_CLass_Fitness.csv", index_col = 0)

a = [SVMClass["TruePositive"].Mean,VitaClass["TruePositive"].Mean,PIMClass["TruePositive"].Mean,PLSClass["TruePositive"].Mean,TestSVMClass["TruePositive"].Mean,TestRFClass["TruePositive"].Mean,TestPLSClass["TruePositive"].Mean]
b = [SVMClass["FalsePositive"].Mean,VitaClass["FalsePositive"].Mean,PIMClass["FalsePositive"].Mean,PLSClass["FalsePositive"].Mean,TestSVMClass["FalsePositive"].Mean,TestRFClass["FalsePositive"].Mean,TestPLSClass["FalsePositive"].Mean]
c = [SVMClass["TruePositive"].STD,VitaClass["TruePositive"].STD,PIMClass["TruePositive"].STD,PLSClass["TruePositive"].STD,TestSVMClass["TruePositive"].STD,TestRFClass["TruePositive"].STD,TestPLSClass["TruePositive"].STD]
d = [SVMClass["FalsePositive"].STD,VitaClass["FalsePositive"].STD,PIMClass["FalsePositive"].STD,PLSClass["FalsePositive"].STD,TestSVMClass["FalsePositive"].STD,TestRFClass["FalsePositive"].STD,TestPLSClass["FalsePositive"].STD]

name = ['SVM-RFE','RF-Vita','RF-PIMP','PLS-VIP','SVM-ALL','RF-ALL','PLS-ALL']
colors=['c', 'b', 'gold', 'm', 'r','seagreen','brown']
figure(num=None, figsize=(10, 6), dpi=80, facecolor='w', edgecolor='k')

for i in range(len(a)):
    plt.scatter(a[i],b[i],label=name[i],color=colors[i])
    plt.errorbar(a[i],b[i],xerr=c[i],yerr=d[i],capsize=2,fmt="none",color=colors[i],linewidth = .25)


matplotlib.rcParams.update({'font.size': 12})
plt.xlabel("Sensitivity",fontsize=12)
plt.ylabel("Specificity",fontsize=12)


plt.show()