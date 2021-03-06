library(fitdistrplus)
library(logspline)
library(moments)

col_width=4

height=col_width
mypar <- function(mfrow) {
par(
    mfrow=mfrow,
#     cex=(1/shrink),
#     cex.axis=mex,
#     cex.lab=mex,
#     cex.main=mex,
#     cex.sub=mex,
#     mex=mex,
#     lwd=(1/shrink),
    oma=c(0,0,0,0),
    xpd=FALSE,
#     tcl=0.5,
    xaxs="i",
    yaxs="i",
    bty="n"
    )
}


date_ranges = read.csv("date_ranges.csv")
revdate_ranges <- date_ranges[rev(rownames(date_ranges)),]
ndate_ranges = length(date_ranges$Count)
date_rangemax = max(date_ranges$Delta)

summary(date_ranges$Delta)
sd(date_ranges$Delta)
skewness(date_ranges$Delta)
kurtosis(date_ranges$Delta)


x=revdate_ranges[revdate_ranges$Count>1,][[3]]/(24*60*60*365*4)
x=revdate_ranges[revdate_ranges$Count>1,][[3]]
weibullparm = fitdist(x, "weibull", method="mle", start=list(shape=1,scale=1), lower=c(0, 0))
weibullparm
gofstat(weibullparm)
# d = dweibull(seq(0, 1, length= length(x)+1), 0.01907475, 2.35506635)
# d2 = dweibull(seq(0, 1, length= length(x)+1), 0.01907475, 2.14096941)
pweibullx = exp(seq(log(1/(24*365.25*4)), log(1), length= length(x)+1))
d = pweibull(pweibullx, weibullparm[[1]][["shape"]], weibullparm[[1]][["scale"]])
library(goftest)
ks.test(x, pweibull,  weibullparm[[1]][["shape"]], weibullparm[[1]][["scale"]])
cvm.test(x, pweibull,  weibullparm[[1]][["shape"]], weibullparm[[1]][["scale"]])
ad.test(x, pweibull,  weibullparm[[1]][["shape"]], weibullparm[[1]][["scale"]])
# d2 = dweibull(seq(0, 1, length= length(x)+1), weibullparm2[[1]][[1]], weibullparm2[[1]][[2]])
# d = d[-1]
# d2 = d2[-1]
# middle_index = 100
# d = d * (x[middle_index]/d[middle_index])
# d2 = d2 * (x[middle_index]/d2[middle_index])

linecolor=rgb(1,0,0)
svg(filename="date_ranges.svg", width=col_width, height=height, 
    family="Latin Modern Roman", pointsize=8)
mypar(c(1,1))
par(mar=c(2.75,3.0,1,1)+0.0)
plot(ecdf(x), 
  main="", ylab="", xlab="", 
  axes=FALSE, log="x",
   xlim=c(1/(24*365.25*4), 1.0),
#   ylim=c(1/24, 365.25*4)/1500
  )
lines(pweibullx, d, col=linecolor)
# lines(seq(1,  length(x)), d2, col=rgb(1,0,1))
legend  ("topleft", 
        legend=c("Empirical CDF",
                 "Beta CDF"), 
        col=c(rgb(0,0,0), linecolor),
        lty=c(1,1),
        bty="n")
axis(1, 
   at=c(1/24,1,7,30,365.25,365.25*4)/(365.25*4),
   labels=c("Hour", "Day", "Week", "Month", "Year", "4Y")
  )
axis(2)
title(ylab="Fraction of Buckets", line=2)
title(xlab="Lifetime less than", line=1.75)

dev.off()

