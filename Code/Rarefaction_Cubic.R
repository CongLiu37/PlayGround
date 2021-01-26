#FIt rarefaction curve
#y(x) = B0+B1*x+B2*x^2+B3*x^3

#ARGUMENT:
#input_file_name, output_file_name

#INPUT:
#A file without header. First column is x, second column is y

#OUTPUT:
#Cubic_<output_file_name>.rda (AIC,B0,B1,B2)

argv = commandArgs(TRUE) #data file, output
source("main.R")

d = read.csv(argv[1], header = F, sep = "\t")
d = as.data.frame(apply(d,2,as.numeric))

mol = lm(data = d, d[,2] ~ poly(d[,1],3,raw=T))

B0_cubic = coef(summary(mol))["(Intercept)",1]
B1_cubic = coef(summary(mol))["poly(d[, 1], 3, raw = T)1",1]
B2_cubic = coef(summary(mol))["poly(d[, 1], 3, raw = T)2",1]
B3_cubic = coef(summary(mol))["poly(d[, 1], 3, raw = T)3",1]

x = d[,1]
y = d[,2]
predic_y = B0_cubic+B1_cubic*x+B2_cubic*x^2+B3_cubic*x^3

AIC_cubic = AIC_calculator(x,y,predic_y,k=3)

save(AIC_cubic,B0_cubic,B1_cubic,B2_cubic,B3_cubic,
     file = paste("Quadratic_",argv[2],sep = ""))
