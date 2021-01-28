#FIt rarefaction curve
#y(x) = log_b(ax+1)

#ARGUMENT:
#input_file_name, output_file_name

#INPUT:
#A file without header. First column is x, second column is y

#OUTPUT:
#7_<output_file_name>.rda (AIC,B0,B1,B2)

argv = commandArgs(TRUE) #data file, output
source("main.R")
library(minpack.lm)

d = read.csv(argv[1], header = F, sep = "\t")
d = as.data.frame(apply(d,2,as.numeric))

x = d[,1]
y = d[,2]

func = function(x,a,b){return(log(a*x+1,base=b))}

b_starts = runif(10,1,1.2)

models = matrix(data=rep(Inf,30),nrow=10,ncol=3)

for (i in 1:10){
  a_start = mean((b_starts[i]^y-1)/x)
  mol = try(
    nlsLM(y ~ func(x,a,b),
          start = list(a=a_start,b=b_starts[i]),
          lower = c(0,1), upper = c(Inf,Inf),
          control = list(maxiter = 500,ftol=0.00001)),silent = T)
  if (as.vector(summary(mol))[2] != "try-error"){
    models[i,2] = coef(summary(mol))["a",1]
    models[i,3] = coef(summary(mol))["b",1]
    predic_y = func(x,models[i,2],models[i,3])
    models[i,1] = AIC_calculator(x,y,predic_y,3)
  }
}

models = as.data.frame(models)
colnames(models) = c("AIC","a","b")

AIC_7=min(models$AIC)

models = subset(models,AIC==AIC_7)
a_7=models$a
b_7=models$b

save(AIC_7,a_7,b_7,file = paste("7_",argv[2],sep = ""))