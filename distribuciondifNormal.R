#-----------------------------------------------------------------
#--------------Valuacion de opciones de cualquier distribucion----
#-----------------------------------------------------------------

Pkg <- c("base","fBasics","fPortfolio","grid","httr","lubridate","PerformanceAnalytics",
         "quantmod","xts","zoo","quadprog","quantmod","ggplot2","timeDate","plyr","Quandl",
         "timeDate","ggplot2","MHadaptive","ks")

inst <- Pkg %in% installed.packages()
if(length(Pkg[!inst]) > 0) install.packages(Pkg[!inst])
instpackages <- lapply(Pkg, library, character.only=TRUE)
#activos
#Paso 1
activos<-c("BIMBOA.MX")
getSymbols.yahoo(Symbols = activos,env=.GlobalEnv,from="2014-11-01",to="2016-03-30")
activo <- do.call(merge, lapply(activos, function(x) Cl(get(x))))

#Paso 2
rendimientosln<-na.omit(diff(log(activo)))

time<-40
k<-54.05
Rf <- 3.5/36000
n<-10000
activo[length(activo)]
st<-51.48

#Paso3
qqnorm(rendimientosln)
qqline(rendimientosln, col = 2)
shapiro.test(as.vector(rendimientosln))

#Paso4

Rf <- 3.5/36000

kernel<-kde((rendimientosln))
plot(kernel$eval.points, kernel$estimate)
x <- seq(-.06,.06, by=.001)
densidad_Kernel <- dkde(x, kernel)
plot(x,densidad_Kernel)

#Paso5

target=function(x){
  dkde(x, kernel)
}
metropolis=function(x,alpha=.03){
  y=runif(1,x-alpha,x+alpha)
  if (runif(1)>target(y)/target(x)) y=x
  return(y)
}

te=time*n*1.2
#x=rep(.0,T)
#for (t in 2:T) x[t]=metropolis(x[t-1])
x<-rkde(te,kernel)
x<-x[(te-round(length(x)/1.2)):(length(x)-1)]
simulaciones<-matrix(x,n,time)

#Paso6
precios<-matrix(0,n,time+1)
precios[,1]<-rep.int(activo[length(activo)],n)
for (i in 2:(time+1)){
  precios[,i]<-precios[,i-1]*exp(simulaciones[,i-1])
}
#Paso7
St<-(precios[,length(precios[1,])])

#Paso8

Call <- pmax(0,St - k)
Put <- pmax(0,k-St)
#Paso9
Call <- mean(Call)
Put<- mean(Put)
#Paso10
Call<-exp(-Rf*time)*Call
Put<-exp(-Rf*time)*Put


Call
Put
sd(rendimientosln)*360
