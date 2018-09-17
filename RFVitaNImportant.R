#! /usr/lib/R/bin/Rscript --vanilla 
library(readr)
library(RFmarkerDetector)
library(randomForest)
library(vita)

args <- commandArgs()

x_DataFileName <- args[7]
y_DataFileName <- args[8]
writeFileName  <- args[9]

x_Data_Pareto <- paretoscale(read_csv(paste(getwd(), x_DataFileName, sep = ""), col_names = FALSE))
y_Data <- read.table(paste(getwd(), y_DataFileName, sep = ""), quote="\"", comment.char="")


if(max(y_Data) != 1){
  y_Data <- t(y_Data)
}

if(max(y_Data) == 1){
  y_Data <- factor(t(y_Data))
}

MetablomicsData.rf = randomForest(x_Data_Pareto,y_Data,ntree = 100, importance = TRUE)

MetablomicsData_cv_vi = CVPVI(x_Data_Pareto,y_Data,k = 2,ntree = 100,ncores = 1)


write.csv(MetablomicsData_cv_vi["cv_varim"], file =   paste(getwd(),   writeFileName,  sep = ""))

