date_ranges = read.csv("date_ranges.csv")
revdate_ranges <- date_ranges[rev(rownames(date_ranges)),]
ndate_ranges = length(date_ranges$Count)
date_rangemax = max(date_ranges$Delta)

summary(date_ranges$Delta)
sd(date_ranges$Delta)
skewness(date_ranges$Delta)
kurtosis(date_ranges$Delta)

library(FAdist)


x=revdate_ranges[revdate_ranges$Count>2,][[3]]/(24*60*60)
x=x/1500
x=revdate_ranges[revdate_ranges$Count>1,][[2]]

weibull3parm = fitdist(x, "weibull3", method="mle", start=list(shape=1,scale=1,thres=0), lower=c(0, 0, -Inf))
weibull3parm
gofstat(weibull3parm)
# d = dweibull3(seq(0, 1, length= length(x)+1), 0.01907475, 2.35506635)
# d2 = dweibull3(seq(0, 1, length= length(x)+1), 0.01907475, 2.14096941)
pweibull3x = exp(seq(log(1/(24*365.25*4)), log(1), length= length(x)+1))
d = pweibull3(pweibull3x, weibull3parm[[1]][["shape"]], weibull3parm[[1]][["scale"]])
library(goftest)
ks.test(x, pweibull3,  weibull3parm[[1]][["shape"]], weibull3parm[[1]][["scale"]])
cvm.test(x, pweibull3,  weibull3parm[[1]][["shape"]], weibull3parm[[1]][["scale"]])
ad.test(x, pweibull3,  weibull3parm[[1]][["shape"]], weibull3parm[[1]][["scale"]])
# d2 = dweibull3(seq(0, 1, length= length(x)+1), weibull3parm2[[1]][[1]], weibull3parm2[[1]][[2]])
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
lines(pweibull3x, d, col=linecolor)
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

