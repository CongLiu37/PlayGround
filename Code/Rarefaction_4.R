#FIt rarefaction curve
#y(x) = a+b/x

#ARGUMENT:
#input_file_name, output_file_name

#INPUT:
#A file without header. First column is x, second column is y

#OUTPUT:
#4_<output_file_name>.rda (AIC,B0,B1,B2)

argv = commandArgs(TRUE) #data file, output
source("main.R")

d = read.csv(argv[1], header = F, sep = "\t")

d = as.data.frame(apply(d,2,as.numeric))

x = d[,1]
y = d[,2]
rec_x = 1/x

mol = lm(y~rec_x)

a_4 = coef(summary(mol))["(Intercept)",1]
b_4 = coef(summary(mol))["rec_x",1]

predic_y = a_4+b_4/x

AIC_4 = AIC_calculator(x,y,predic_y,k=3)

save(AIC_4,a_4,b_4,
     file = paste("4_",argv[2],sep = ""))