


RSS = function(x, y, predict_y){
  #Sum of squares
  
  #ARGUMENT
  #independent value, response value, predicted response value
  Rss = sum((y-predic_y)^2)
  return(Rss)
}

likelihood = function(x, y, predic_y){
  #Likelihood
  
  #ARGUMENT
  #independent value, response value, predicted response value
  Rss = RSS(x,y,predic_y)
  n = length(x)
  L = -0.5*n*log(Rss/n)
  return(L)
}

AIC_calculator = function(x, y, predic_y, k){
  #Akaike information criterion
  
  #ARGUMENT
  #independent value, response value, predicted response value, model complexity
  L = likelihood(x,y,ptrdic_y)
  AIC = -2*L+2*k
  return(AIC)
}
