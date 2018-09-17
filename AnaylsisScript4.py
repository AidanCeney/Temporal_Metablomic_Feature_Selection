import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import CompareMethods

GC = "Res_GC/"
LC = "Res_LC/"
Targeted = "Res_Targeted/"
Type = "PLS"
Mode = "_Class_"

ListSelected = [GC + Type + Mode + "Selection.csv",LC +  Type + Mode + "Selection.csv",Targeted + Type + Mode + "Selection.csv"]
ListOfMethods = ["EI","RP","Targeted"]

CompareMethods.pltSTD(ListSelected,ListOfMethods,"")
