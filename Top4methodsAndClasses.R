install.packages("plyr")
install.packages("data.table")
library(plyr)
library(data.table)
df<-read.csv("method_freq.csv",sep=",",header = FALSE)
colnames(df)<-c("Method","Count")
df["QualifiedClassName"]<-gsub("::.*$","",df$Method)
df_sorted<-arrange(df,-Count)
plot(factor(df_sorted[1:4,"Method"]), df_sorted[1:4,"Count"],xlab="MethodName",ylab="Frequency",main = "Top 4 methods",col="red",asp=10:9)

x<-factor(df_sorted[1:4,"Method"])
y<-df_sorted[1:4,"Count"]

barplot(y,names.arg=x, col=c("red","blue","orange","purple"),xlab="MethodName",ylab="Frequency",main = "Top 4 methods")


a<-aggregate(df$Count, by=list(df$QualifiedClassName), FUN=sum)
a_sorted<-arrange(a,-x)
plot(factor(a_sorted[1:4,"Group.1"]), a_sorted[1:4,"x"], xlab="ClassName", ylab="Frequency", main="Top 4 Classes")


x<-factor(a_sorted[1:4,"Group.1"])
y<-a_sorted[1:4,"x"]

barplot(y, names.arg=x, col=c("red","blue","orange","purple"))