#FIt rarefaction curve
#y(x) = a*x/(1+b*x)

#ARGUMENT:
#input_file_name, output_file_name

#INPUT:
#A file without header. First column is x, second column is y

#OUTPUT:
#5_<output_file_name>.rda (AIC,B0,B1,B2)

argv = commandArgs(TRUE) #data file, output
source("main.R")

d = read.csv(argv[1], header = F, sep = "\t")

d = as.data.frame(apply(d,2,as.numeric))

x = d[,1]
y = d[,2]
rec_x = 1/x
rec_y = 1/y

mol = lm(rec_y~rec_x)


a_5 = 1/coef(summary(mol))["rec_x",1]
b_5 = coef(summary(mol))["(Intercept)",1]/coef(summary(mol))["rec_x",1]

predic_y = a_5*x/(1+b_5*x)

AIC_5 = AIC_calculator(x,y,predic_y,k=3)

save(AIC_5,a_5,b_5,
     file = paste("5_",argv[2],sep = ""))