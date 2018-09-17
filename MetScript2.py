import pandas as pd
import SVMRFEAnalysis  as aSVM
import RFAnalysis      as aRF
import PLSVIPAnalaysis as aPLS
import MetFileParser
import SelectFeatures




Test = MetFileParser.readMetaboliteAndCondition(["Raw Data/EI_perCell.csv"],[1],[[0,2,3,4,5]],list(range(68)))
Beg = "Res_GC/"

Results = SelectFeatures.RepeatEvaluateMethod(Test,128,32,4,aSVM.EvaluateRegresionSVM)

pd.DataFrame(data=Results['AVGSTDFitness']).to_csv(Beg + "Test_SVM_REG_Fitness.csv")  
Results['y_Test_Pedict'].to_csv(Beg  + "Test_SVM_REG_yValues.csv")

Results = SelectFeatures.RepeatEvaluateMethod(Test,128,32,4,aSVM.EvaluateClassSVM)
pd.DataFrame(data=Results['AVGSTDFitness']).to_csv(Beg + "Test_SVM_Class_Fitness.csv")  
Results['y_Test_Pedict'].to_csv(Beg  + "Test_SVM_Class_yValues.csv")


Results = SelectFeatures.RepeatEvaluateMethod(Test,128,32,4,aRF.EvaluateRegresionRF)
pd.DataFrame(data=Results['AVGSTDFitness']).to_csv(Beg + "Test_RF_REG_Fitness.csv")  
Results['y_Test_Pedict'].to_csv(Beg  + "Test_RF_REG_yValues.csv")

Results = SelectFeatures.RepeatEvaluateMethod(Test,128,32,4,aRF.EvaluateClassRF)

pd.DataFrame(data=Results['AVGSTDFitness']).to_csv(Beg + "Test_RF_Class_Fitness.csv")  
Results['y_Test_Pedict'].to_csv(Beg + "Test_RF_Class_yValues.csv")



Results = SelectFeatures.RepeatEvaluateMethod(Test,128,32,4,aPLS.EvaluateClassPLS)
pd.DataFrame(data=Results['AVGSTDFitness']).to_csv(Beg + "Test_PLS_CLass_Fitness.csv")  
Results['y_Test_Pedict'].to_csv(Beg  + "Test_PLS_Class_yValues.csv")

Results = SelectFeatures.RepeatEvaluateMethod(Test,128,32,4,aPLS.EvaluateRegresionPLS)
pd.DataFrame(data=Results['AVGSTDFitness']).to_csv(Beg + "Test_PLS_REG_Fitness.csv")  
Results['y_Test_Pedict'].to_csv(Beg + "Test_PLS_REG_yValues.csv")

