#FIt rarefaction curve
#y(x) = B0+B1*x+B2*x^2+B3*x^3

#ARGUMENT:
#input_file_name, output_file_name

#INPUT:
#A file without header. First column is x, second column is y

#OUTPUT:
#2_<output_file_name>.rda (AIC,B0,B1,B2)

argv = commandArgs(TRUE) #data file, output
source("main.R")

d = read.csv(argv[1], header = F, sep = "\t")
d = as.data.frame(apply(d,2,as.numeric))

mol = lm(data = d, d[,2] ~ poly(d[,1],3,raw=T))

B0_2 = coef(summary(mol))["(Intercept)",1]
B1_2 = coef(summary(mol))["poly(d[, 1], 3, raw = T)1",1]
B2_2 = coef(summary(mol))["poly(d[, 1], 3, raw = T)2",1]
B3_2 = coef(summary(mol))["poly(d[, 1], 3, raw = T)3",1]

x = d[,1]
y = d[,2]
predic_y = B0_2+B1_2*x+B2_2*x^2+B3_2*x^3

AIC_2 = AIC_calculator(x,y,predic_y,k=5)

save(AIC_2,B0_2,B1_2,B2_2,B3_2,
     file = paste("2_",argv[2],sep = ""))
