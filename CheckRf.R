#! /usr/local/bin/Rscript --vanilla 
library(readr)
library(RFmarkerDetector)
library(randomForest)
library(vita)

args <- commandArgs()
XTrainFileName = args[7]
YTrainFileName = args[8]
XTestFileName = args[9]
YTestFileName = args[10]




y_Data <- read.table(paste(getwd(), YTrainFileName,sep = ""), quote="\"", comment.char="")
if (max(y_Data) == 1){
  ny_Data <- factor(t(y_Data))
}
if(max(y_Data) > 1){
  ny_Data <- t(y_Data)

}

x_Data_Pareto <- paretoscale(read_csv(paste(getwd(), XTrainFileName ,sep = ""), col_names = FALSE))
x_Data_Pareto_Test <- paretoscale(read_csv(paste(getwd(), XTestFileName ,sep = ""), col_names = FALSE))

MetablomicsData.rf = randomForest(x_Data_Pareto,ny_Data,xtest = x_Data_Pareto_Test,ntree = 100, importance = TRUE)
write.csv(MetablomicsData.rf$test$predicted, file = paste(getwd(), YTestFileName ,sep = "") )



