import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import FeatureSelectionUtillFunctions as fsutill
import pylab

def getMethodeOverlap(ListOfFiles,ListOfMethods):

    ListSortedNames = []
    for File in ListOfFiles:
        ListSortedNames.append(list(pd.read_csv(File,index_col = 0).sort_values("VarImp",ascending = False).index))

    DictOfMetabolites = {}
    
    count = 0
    for Names in ListSortedNames:
        internalCount = 0
        for Metabolites in Names:
            if(DictOfMetabolites.get(Metabolites) == None):
                DictOfMetabolites[Metabolites] = {"RelIndexs": [internalCount],"List_Of_Methods": [ListOfMethods[count]],"NumSelected": 1}
            else:
                DictOfMetabolites[Metabolites]["RelIndexs"].append(internalCount)
                DictOfMetabolites[Metabolites]["List_Of_Methods"].append(ListOfMethods[count])
                DictOfMetabolites[Metabolites]["NumSelected"] += 1
            internalCount += 1
        count += 1
    
    for Metabolite in DictOfMetabolites:
        DictOfMetabolites[Metabolite]["STD"]  = np.std(DictOfMetabolites[Metabolite]["RelIndexs"])
        DictOfMetabolites[Metabolite]["Mean"] = np.mean(DictOfMetabolites[Metabolite]["RelIndexs"])
    return pd.DataFrame(data = DictOfMetabolites) 

def getNumMethodeOverlap(dfDictOfMetabolites):
    DictListMethod = {}
    for index, row in dfDictOfMetabolites.iterrows():
        if(index == "List_Of_Methods"):
            count = 0
            for Name, methods in row.iteritems():
                for method in methods:
                    if(DictListMethod.get(method) == None):
                        DictListMethod[method] = [count]
                    else:
                        DictListMethod[method].append(count)
                count += 1
    return DictListMethod

def CombineMethodes(ListMethod):
    ret = ""
    First = True
    for Method in ListMethod:
        if First:
            First = False
            ret += Method
        else:
            ret += ("-" + Method)
    return ret

def pltSTD(ListOfFiles,ListOfType,atittle):
    
    count = 0
    figData = pylab.figure()
    ax = pylab.gca()

    for File in ListOfFiles:
        tmpDF = pd.read_csv(File,index_col = 0).sort_values("VarImp",ascending = False)
        tmpDF["%STD"] = tmpDF["STD"] / tmpDF["VarImp"]
        plt.scatter(range(len(list(tmpDF["%STD"]))),list(tmpDF["%STD"]),label=ListOfType[count])
        count += 1
    
    plt.xlabel("Relative Importance")
    plt.ylabel("% Standard Deviation")
    plt.title(atittle)
    figLegend = pylab.figure(figsize = (1.5,1.3))
    pylab.figlegend(*ax.get_legend_handles_labels(), loc = 'upper left',ncol=3)
    plt.show()
    return
        


    

