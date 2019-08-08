library(ggplot2)
library(reshape2)

datos1<-read.table("final.csv",sep=",",header = T)


datos2melt<-melt(datos8, id=c("NOM_RBD","NOM_DEPE"))

ggplot(datos2melt[which(datos2melt$variable %in% c("ERROR")),])+
  geom_density(aes(x=value,col=NOM_DEPE,fill=NOM_DEPE),alpha=0.2)+
  facet_grid(.~variable)
summary(lm(datos8$ALUMNOS_TOTAL~datos8$ERROR))

#sqrt(mean((datos2$ALUMNOS_NO_VULNERABLES-datos2$MAT_NO_VULNERABLES)^2))
#sqrt(mean((datos2$ALUMNOS_VULNERABLES-datos2$MAT_VULNERABLES)^2))