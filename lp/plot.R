top1 = read.csv("top1.csv")
methods = list.files(pattern="*.csv")
data = lapply(setNames(methods, make.names(gsub("*.csv$", "", methods))), 
         read.csv)
nmethods = length(data)
colors <- rainbow(nmethods)
linetype <- rep(1:6, 10)
plotchar <- rep(c(0, 1, 2, 3, 4, 5, 6, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25), 2)    

plot(top1$n, top1$b3f, type='n', ylim=c(0.0,1.0))
for (i in 1:nmethods) {
    method <- data[[i]]
    metric <- "b3p"
    lines(method[["n"]], method[[metric]], type='b', lwd=1.5,
    lty=linetype[i], col=colors[i], pch=plotchar[i])
}
title("B3F", "BCubed F1-Score")
legend("bottomleft", legend=names(data), col=colors, pch=plotchar, lty=linetype,
    title="Method")
