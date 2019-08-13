library(ggplot2)
library(reshape2)
library(MASS)
library(doBy)
library(FSA)
library(sfsmisc)

# - Obtener moda
get_mode <- function(v) {
  uniqv <- unique(v)
  uniqv[which.max(tabulate(match(v, uniqv)))]
}

# - Analisis de densidades y regresion
analyze <- function(data){
  
  datamelt <- melt(data, id=c("NOM_RBD","NOM_DEPE"))

  print(
    ggplot(
      datamelt[which(datamelt$variable %in% c("DIFERENCIA_VULNERABLES")),]
    ) +
    geom_density(
      aes(x=value, col=NOM_DEPE, fill=NOM_DEPE), 
      alpha=0.2
    ) +
    facet_grid(.~variable)
  )
  
  regression <- (rlm(data$DIFERENCIA_VULNERABLES~data$ALUMNOS_TOTAL))
  
  print(summary(data$DIFERENCIA_VULNERABLES))
  print(summary(data$DIFERENCIA_VULNERABLES[-32]))
  print(get_mode(data$DIFERENCIA_VULNERABLES))
  print(shapiro.test(caso_3$DIFERENCIA_VULNERABLES))
  print(shapiro.test(caso_3$DIFERENCIA_VULNERABLES[-32]))

  plot(density(data$DIFERENCIA_VULNERABLES))
  plot(
    data$DIFERENCIA_VULNERABLES ~ data$ALUMNOS_TOTAL,
    ylab="Residuo", 
    xlab="Total de alumnos"
  )
  
  abline(
    regression$coefficients[1], 
    regression$coefficients[2],
    col='red'
  )
  print(summary(regression))
  print(f.robftest(regression))
}

caso_1 <-read.table("caso_1.csv", sep=",", header = T)
caso_2 <-read.table("caso_2.csv", sep=",", header = T)
caso_3 <-read.table("caso_3.csv", sep=",", header = T)


analyze(caso_1)
#analyze(caso_2)
#analyze(caso_3)


datos <- data.frame(
  id=1: (nrow(caso_1) -1),
  caso_1 = caso_1$DIFERENCIA_VULNERABLES[-32], 
  caso_2 = caso_2$DIFERENCIA_VULNERABLES[-32],
  caso_3 = caso_3$DIFERENCIA_VULNERABLES[-32]
)

datos <- melt(datos, id='id')

head(datos)
bartlett.test(value~variable, datos)
modelo <- aov(value~variable, data=datos)
summary(modelo)
