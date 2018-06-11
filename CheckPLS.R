#! /usr/lib/R/bin/Rscript --vanilla 
library(readr)
library(RFmarkerDetector)
library(mixOmics)

args <- commandArgs()

XTrainFileName = args[7]
YTrainFileName = args[8]
XTestFileName = args[9]
YTestFileName = args[10]




y_Data <- read.table(paste(getwd(), YTrainFileName,sep = ""), quote="\"", comment.char="")
x_Data_Pareto <- paretoscale(read_csv(paste(getwd(), XTrainFileName ,sep = ""), col_names = FALSE))

if(max(y_Data) == 1){
  ny_Data <- factor(t(y_Data))

  apls <- plsda(x_Data_Pareto,ny_Data)
}
if(max(y_Data) > 1){

  ny_Data <- y_Data

  apls <- pls(x_Data_Pareto,ny_Data)
}

x_Data_Pareto_Test <- paretoscale(read_csv(paste(getwd(), XTestFileName ,sep = ""), col_names = FALSE))
plsRes <- predict(apls,x_Data_Pareto_Test,dist = "max.dist")
write.csv(plsRes$predict, file = paste(getwd(), YTestFileName ,sep = ""))



