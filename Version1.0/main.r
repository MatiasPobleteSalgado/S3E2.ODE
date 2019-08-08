library(ggplot2)
library(reshape2)

datos<-read.table("final.csv",sep=",",header = T)

datosmelt<-melt(datos, id=c("NOM_RBD","NOM_DEPE"))

ggplot(
  datosmelt[
    which(datosmelt$variable %in% c("DIFERENCIA_VULNERABLES")),
    ]
) +
geom_density(
  aes(
    x=value,
    col=NOM_DEPE,
    fill=NOM_DEPE
  ),
  alpha=0.2
) +
facet_grid(.~variable)

summary(lm(datos$ALUMNOS_TOTAL~datos$DIFERENCIA_VULNERABLES))

sqrt(mean((datos$ALUMNOS_NO_VULNERABLES-datos$MAT_NO_VULNERABLES)^2))
