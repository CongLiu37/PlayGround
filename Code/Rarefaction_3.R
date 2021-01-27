#FIt rarefaction curve
#y(x) = a*x^b
#log(y(x)) = log(a) + b*log(x)

#ARGUMENT:
#input_file_name, output_file_name

#INPUT:
#A file without header. First column is x, second column is y

#OUTPUT:
#3_<output_file_name>.rda (AIC,B0,B1,B2)

argv = commandArgs(TRUE) #data file, output
source("main.R")

d = read.csv(argv[1], header = F, sep = "\t")

d = as.data.frame(apply(d,2,as.numeric))

x = d[,1]
y = d[,2]

logx = log(x)
logy = log(y)

mol = lm(logy ~ logx)

a_3 = exp(coef(summary(mol))["(Intercept)",1])
b_3 = coef(summary(mol))["logx",1]

predic_y = a_3*x^b_3

AIC_3 = AIC_calculator(x,y,predic_y,k=3)

save(AIC_3,a_3,b_3,
     file = paste("3_",argv[2],sep = ""))
