date_ranges = read.csv("date_ranges.csv")
revdate_ranges <- date_ranges[rev(rownames(date_ranges)),]
ndate_ranges = length(date_ranges$Count)
date_rangemax = max(date_ranges$Delta)

summary(date_ranges$Delta)
sd(date_ranges$Delta)
skewness(date_ranges$Delta)
kurtosis(date_ranges$Delta)


x=revdate_ranges[revdate_ranges$Count>2,][[3]]/(24*60*60)
x=x/1500
x=revdate_ranges[revdate_ranges$Count>1,][[2]]

ginvgaussparm = fitdist(x, "ginvgauss", method="mle", start=list(s=1,m=1,f=1), lower=c(0, 0))
ginvgaussparm
gofstat(ginvgaussparm)
# d = dginvgauss(seq(0, 1, length= length(x)+1), 0.01907475, 2.35506635)
# d2 = dginvgauss(seq(0, 1, length= length(x)+1), 0.01907475, 2.14096941)
pginvgaussx = exp(seq(log(1/(24*365.25*4)), log(1), length= length(x)+1))
d = pginvgauss(pginvgaussx, ginvgaussparm[[1]][["s"]], ginvgaussparm[[1]][["m"]], ginvgaussparm[[1]][["f"]])
library(goftest)
ks.test(x, pginvgauss,  ginvgaussparm[[1]][["s"]], ginvgaussparm[[1]][["m"]], ginvgaussparm[[1]][["f"]])
cvm.test(x, pginvgauss,  ginvgaussparm[[1]][["s"]], ginvgaussparm[[1]][["m"]], ginvgaussparm[[1]][["f"]])
ad.test(x, pginvgauss,  ginvgaussparm[[1]][["s"]], ginvgaussparm[[1]][["m"]], ginvgaussparm[[1]][["f"]])
# d2 = dginvgauss(seq(0, 1, length= length(x)+1), ginvgaussparm2[[1]][[1]], ginvgaussparm2[[1]][[2]])
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
lines(pginvgaussx, d, col=linecolor)
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

