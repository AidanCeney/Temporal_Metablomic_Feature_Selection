import pandas as pd
import SVMRFEAnalysis  as aSVM
import RFAnalysis      as aRF
import PLSVIPAnalaysis as aPLS
import MetFileParser
import SelectFeatures


Test = MetFileParser.readMetaboliteAndCondition(["Raw Data/NA_perCell.csv","Raw Data/AA_perCell.csv","Raw Data/hil_perCell.csv"],[1,1,1],[[0,2,3,4,5],[0,2,3,4,5,6],[0,2,3,4,5,6]],list(range(72)))
#Test = MetFileParser.readMetaboliteAndCondition(["Raw Data/RP_perCell.csv"],[1],[[0,2,3,4,5]],list(range(70)))

Beg = "Res_GC/"
#Test = MetFileParser.readMetaboliteAndCondition(["Raw Data/EI_perCell.csv"],[1],[[0,2,3,4,5]],list(range(68)))
print(len(Test.getListOfMetabolites()))
'''
Results = SelectFeatures.EvaluateSelectionWithDoubleCFV(Test,128,32,4,1,100,aSVM.SelectWithSVMRegresion,aSVM.MergeResultsWraper,aSVM.EvaluateRegresionSVM)
pd.DataFrame(data=Results['AVGSTDFitness']).to_csv(Beg + "SVM_REG_Fitness.csv")  
Results['TotalSelection'].to_csv(Beg + "SVM_REG_Selection.csv") 
Results['y_Test_Pedict'].to_csv(Beg  + "SVM_REG_yValues.csv")


Results = SelectFeatures.EvaluateSelectionWithDoubleCFV(Test,128,32,4,1,100,aSVM.SelectWithSVMClass,aSVM.MergeResultsWraper,aSVM.EvaluateClassSVM)
pd.DataFrame(data=Results['AVGSTDFitness']).to_csv(Beg + "SVM_Class_Fitness.csv")  
Results['TotalSelection'].to_csv(Beg + "SVM_Class_Selection.csv") 
Results['y_Test_Pedict'].to_csv(Beg  + "SVM_Class_yValues.csv")

Beg = "Res_LC/"
Test = MetFileParser.readMetaboliteAndCondition(["Raw Data/RP_perCell.csv"],[1],[[0,2,3,4,5]],list(range(70)))

Results = SelectFeatures.EvaluateSelectionWithDoubleCFV(Test,128,32,5,1,200,aSVM.SelectWithSVMRegresion,aSVM.MergeResultsWraper,aSVM.EvaluateRegresionSVM)
pd.DataFrame(data=Results['AVGSTDFitness']).to_csv(Beg + "SVM_REG_Fitness.csv")  
Results['TotalSelection'].to_csv(Beg + "SVM_REG_Selection.csv") 
Results['y_Test_Pedict'].to_csv(Beg  + "SVM_REG_yValues.csv")

Results = SelectFeatures.EvaluateSelectionWithDoubleCFV(Test,128,32,5,1,200,aSVM.SelectWithSVMClass,aSVM.MergeResultsWraper,aSVM.EvaluateClassSVM)
pd.DataFrame(data=Results['AVGSTDFitness']).to_csv(Beg + "SVM_Class_Fitness.csv")  
Results['TotalSelection'].to_csv(Beg + "SVM_Class_Selection.csv") 
Results['y_Test_Pedict'].to_csv(Beg  + "SVM_Class_yValues.csv")


Beg = "Res_Targeted/"
Test = MetFileParser.readMetaboliteAndCondition(["Raw Data/NA_perCell.csv","Raw Data/AA_perCell.csv","Raw Data/hil_perCell.csv"],[1,1,1],[[0,2,3,4,5],[0,2,3,4,5,6],[0,2,3,4,5,6]],list(range(72)))

Results = SelectFeatures.EvaluateSelectionWithDoubleCFV(Test,128,32,6,1,75,aSVM.SelectWithSVMRegresion,aSVM.MergeResultsWraper,aSVM.EvaluateRegresionSVM)
pd.DataFrame(data=Results['AVGSTDFitness']).to_csv(Beg + "SVM_REG_Fitness.csv")  
Results['TotalSelection'].to_csv(Beg + "SVM_REG_Selection.csv") 
Results['y_Test_Pedict'].to_csv(Beg  + "SVM_REG_yValues.csv")

Results = SelectFeatures.EvaluateSelectionWithDoubleCFV(Test,128,32,6,1,75,aSVM.SelectWithSVMClass,aSVM.MergeResultsWraper,aSVM.EvaluateClassSVM)
pd.DataFrame(data=Results['AVGSTDFitness']).to_csv(Beg + "SVM_Class_Fitness.csv")  
Results['TotalSelection'].to_csv(Beg + "SVM_Class_Selection.csv") 
Results['y_Test_Pedict'].to_csv(Beg  + "SVM_Class_yValues.csv")
'''
