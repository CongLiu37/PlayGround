#FIt rarefaction curve
#y(x) = B0+B1*x+B2*x^2

#ARGUMENT:
#input_file_name, output_file_name

#INPUT:
#A file without header. First column is x, second column is y

#OUTPUT:
#Quadratic_<output_file_name>.rda (AIC,B0,B1,B2)

argv = commandArgs(TRUE) #data file, output
source("main.R")

d = read.csv(argv[1], header = F, sep = "\t")
d = as.data.frame(apply(d,2,as.numeric))

mol = lm(data = d, d[,2] ~ poly(d[,1],2,raw=T))

B0_quadratic = coef(summary(mol))["(Intercept)",1]
B1_quadratic = coef(summary(mol))["poly(d[, 1], 2, raw = T)1",1]
B2_quadratic = coef(summary(mol))["poly(d[, 1], 2, raw = T)2",1]

x = d[,1]
y = d[,2]
predic_y = B0_quadratic+B1_quadratic*x+B2_quadratic*x^2

AIC_quadratic = AIC_calculator(x,y,predic_y,k=2)

save(AIC_quadratic,B0_quadratic,B1_quadratic,B2_quadratic,
     file = paste("Quadratic_",argv[2],sep = ""))