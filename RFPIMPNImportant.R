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
pimp.MetablomicsData.varImp.cl<-PIMP(x_Data_Pareto,y_Data,MetablomicsData.rf,S=100)
pimp.MetablomicsData.cl = PimpTest(pimp.MetablomicsData.varImp.cl,para = TRUE)

write.csv(pimp.MetablomicsData.cl["VarImp"], file =   paste(getwd(),   writeFileName,  sep = ""))

