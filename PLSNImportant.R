#! /usr/local/bin/Rscript --vanilla 
library(readr)
library(RFmarkerDetector)
library(mixOmics)

args <- commandArgs()

x_DataFileName <- args[7]
y_DataFileName <- args[8]
writeFileName  <- args[9]

x_Data_Pareto <- paretoscale(read_csv(paste(getwd(), x_DataFileName, sep = ""), col_names = FALSE))
y_Data <- read.table(paste(getwd(), y_DataFileName, sep = ""), quote="\"", comment.char="")

if(max(y_Data) == 1){
  ny_Data <- factor(t(y_Data))
  
  apls <- plsda(x_Data_Pareto,ny_Data)
}
if(max(y_Data) > 1){
  
  ny_Data <- y_Data
  
  apls <- pls(x_Data_Pareto,ny_Data)
}

VIPpls <- vip(apls)
write.csv(VIPpls, file =   paste(getwd(),   writeFileName,  sep = ""))

