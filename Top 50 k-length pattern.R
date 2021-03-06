install.packages("plyr")
install.packages("data.table")
library(plyr)
library(data.table)
df<-read.csv("100-length.csv",sep=",",header=FALSE)
l<-length(df)
colnames(df) <- paste("col", 2:l-1, sep = "")
colnames(df)[l]<-"Count"
df["SequenceNo"]<-seq(1:nrow(df))
df["Sequence"]<-do.call(paste0, df[1:l-1])
df_sorted<-arrange(df,-Count)
barplot(df_sorted[1:50,"Count"], names.arg = df_sorted[1:50,"SequenceNo"],col="purple",xlab="Pattern ID",ylab="Frequency",main="Distribution of 5-length patterns")