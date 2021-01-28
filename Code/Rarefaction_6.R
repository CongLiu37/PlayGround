#FIt rarefaction curve
#y(x) = b-b*a^x

#ARGUMENT:
#input_file_name, output_file_name

#INPUT:
#A file without header. First column is x, second column is y

#OUTPUT:
#6_<output_file_name>.rda (AIC,a,b)

argv = commandArgs(TRUE) #data file, output
source("main.R")
library(minpack.lm)

d = read.csv(argv[1], header = F, sep = "\t")
d = as.data.frame(apply(d,2,as.numeric))

x = d[,1]
y = d[,2]

b_start = max(y)

a_start = exp(log((b_start-y)/b_start)/x)
c = which(a_start==0)
a_start = a_start[-c]
a_start = mean(a_start)

func = function(x,a,b){return(b-b*a^x)}

mol = try(nlsLM(y ~ func(x,a,b),
          start = list(a=a_start,b=b_start),
          lower = c(0,0), upper = c(1,Inf),
          control = list(maxiter = 500,ftol=0.00001)),silent = T)

if (as.vector(summary(mol))[2] != "try-error"){
  a_6 = coef(summary(mol))["a",1]
  b_6 = coef(summary(mol))["b",1]
  predic_y = func(x,a_6,b_6)
  AIC_6 = AIC_calculator(x,y,predic_y,3)
}else{print("Fail")}

save(AIC_6,a_6,b_6,file = paste("6_",argv[2],sep = ""))
