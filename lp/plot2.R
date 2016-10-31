library(fitdistrplus)
library(logspline)
library(moments)

shrink = 2
mex = shrink/1.255
linesx = 2.0


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


pareto.MLE <- function(X)
{
   n <- length(X)
   m <- min(X)
   a <- n/sum(log(X)-log(m))
   return( c(m,a) ) 
}

mymoment <- function(x, order) {
  return(moment(x, order))
}

col_width=4

height=col_width

packages = read.csv("packages.csv")
revpackages <- packages[rev(rownames(packages)),]
options(scipen=5)
npackages = length(packages$Count)
packagemax = max(packages$Count)

require(zipfR)
packagesspc = tfl2spc(tfl(packages$Count))
packagesfzm = lnre("fzm", packagesspc)
packagesfzm
packagesfzm.spc = lnre.spc(packagesfzm, N(packagesfzm))
svg(filename="packagesfzm.svg", width=col_width, height=height, 
    family="Latin Modern Roman", pointsize=8)
mypar(c(1,1))
par(mar=c(2.75,3.0,1,1)+0.0)
plot(packagesspc, packagesfzm.spc, log="xy", 
                  xlab="",
                  ylab="")
title(xlab="Number of Crashes", line=1.75)
title(ylab="Number of Packages", line=2)
legend("topright", 
       legend=c("Empirical Data", "Finite Zipf-Mandelbrot"),
       pch=c(1,3),
       col=c(rgb(0,0,0), rgb(1,0,0),
       lty=c(1,1)),
       bty='n'
       )
dev.off()


svg(filename="packages.svg", width=col_width, height=height, 
    family="Latin Modern Roman", pointsize=8)
mypar(c(1,1))
par(mar=c(2.75,3.0,1,1)+0.0)
plot(seq(1, npackages), revpackages$Count, 
  type="h",
  main="", ylab="", xlab="", 
  axes=FALSE, log="xy",
  xlim=c(0.8, npackages+1),
  ylim=c(1, packagemax))
axis(2, at=c(1,2,5,10,20,50,100,200,500,1000,packagemax)) 
axis(1, at=c(1,2,5,10,20,50,100,200,500,1000,npackages))
title(xlab="Package", line=1.75)
title(ylab="Crashes Seen", line=2)
dev.off()



buckets = read.csv("buckets_dist.csv")
revbuckets <- buckets[rev(rownames(buckets)),]
nbuckets = length(buckets$Count)
bucketmax = max(buckets$Count)

bucketsspc = tfl2spc(tfl(buckets$Count))
bucketsfzm = lnre("fzm", bucketsspc)
bucketsfzm
bucketsfzm.spc = lnre.spc(bucketsfzm, N(bucketsfzm))
svg(filename="bucketsfzm.svg", width=col_width, height=height, 
    family="Latin Modern Roman", pointsize=8)
mypar(c(1,1))
par(mar=c(2.75,3.0,1,1)+0.0)
plot(bucketsspc, bucketsfzm.spc, log="xy", 
                  xlab="",
                  ylab="")
title(xlab="Number of Crashes", line=1.75)
title(ylab="Number of Buckets", line=2)
legend("topright", 
       legend=c("Empirical Data", "Finite Zipf-Mandelbrot"),
       pch=c(1,3),
       col=c(rgb(0,0,0), rgb(1,0,0),
       lty=c(1,1)),
       bty='n'
       )
dev.off()


svg(filename="buckets.svg", width=col_width, height=height, 
    family="Latin Modern Roman", pointsize=8)
mypar(c(1,1))
par(mar=c(2.75,3.0,1,1)+0.0)
plot(seq(1, nbuckets), revbuckets$Count, 
  type="h",
  main="", ylab="", xlab="", 
  axes=FALSE, log="xy",
  xlim=c(0.8, nbuckets+1),
  ylim=c(1, bucketmax))
axis(2, at=c(1,2,5,10,20,50,bucketmax)) 
axis(1, at=c(1,2,5,10,20,50,100,200,500,1000,nbuckets))
title(xlab="Bucket", line=1.75)
title(ylab="Crashes", line=2)
dev.off()



# svg(filename="buckets.svg", width=col_width, height=height, 
#     family="Latin Modern Roman", pointsize=10)
# mypar(c(1,1))
# par(mar=c(1.75,2.0,1,1)+0.0)
# plot(seq(1, nbuckets), revbuckets$Count, 
#   type="h",
#   main="", ylab="", xlab="", 
#   axes=FALSE, log="xy",
#   xlim=c(0.8, nbuckets+1),
#   ylim=c(1, bucketmax))
# axis(2, mgp=c(1.25, 0.25, 0), lwd=(1/shrink), at=c(1,2,5,10,20,50,bucketmax)) 
# axis(1, mgp=c(1.5, 0.5, 0), lwd=(1/shrink), at=c(1,2,5,10,20,50,100,200,500,1000,nbuckets))
# # paretoparm = fitdist(revbuckets$Count, "pareto", method="mme", order=c(1,1), memp=mymoment)
# # paretoparm
# # pareto.MLE(revbuckets$Count)
# # paretofit = dpareto(seq(0, 1000), 0.1, 300) * sum(table(revbuckets$Count))
# # lines(seq(0,  1000), paretofit, col=rgb(1,0,0), cex=linesx)
# title(ylab="Crashes", line=1.0)
# title(xlab="Bucket", line=1.25)
# dev.off()


# ================================

date_ranges = read.csv("date_ranges.csv")
revdate_ranges <- date_ranges[rev(rownames(date_ranges)),]
ndate_ranges = length(date_ranges$Count)
date_rangemax = max(date_ranges$Delta)
x=revdate_ranges[revdate_ranges$Count>2,][[3]]/(24*60*60)
x=x/1500
betaparm = fitdist(x, "beta", method="mme")
betaparm
gofstat(betaparm)
betaparm2 = fitdist(x, "beta", method="mle")
betaparm2
# d = dbeta(seq(0, 1, length= length(x)+1), 0.01907475, 2.35506635)
# d2 = dbeta(seq(0, 1, length= length(x)+1), 0.01907475, 2.14096941)
d = pbeta(seq(0, 1, length= length(x)+1), betaparm[[1]][[1]], betaparm[[1]][[2]])
library(goftest)
ks.test(x, pbeta,  betaparm[[1]][[1]], betaparm[[1]][[2]])
cvm.test(x, pbeta,  betaparm[[1]][[1]], betaparm[[1]][[2]])
ad.test(x, pbeta,  betaparm[[1]][[1]], betaparm[[1]][[2]])
# d2 = dbeta(seq(0, 1, length= length(x)+1), betaparm2[[1]][[1]], betaparm2[[1]][[2]])
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
  axes=FALSE, log="y",
#   xlim=c(0.8, length(x)+1),
  ylim=c(1/24, 365.25*4)/1500
  )
lines(seq(1,  length(d))/length(d), d, col=linecolor)
# lines(seq(1,  length(x)), d2, col=rgb(1,0,1))
legend  ("topright", 
        legend=c("Empirical Distribution",
                 "Beta Distribution"), 
        col=c(rgb(0,0,0), linecolor),
        lty=c(1,1),
        bty="n")
axis(2, 
  at=c(1/24,1,7,30,365.25,365.25*4)/1500,
  labels=c("Hour", "Day", "Week", "Month", "Year", "4Y")
  )
axis(1)
title(ylab="Lifetime", line=2)
title(xlab="Bucket #", line=1.75)

dev.off()
quit()

# 
# descdist(revdate_ranges$Delta, discrete=FALSE, boot=100)
# 
# hist(revdate_ranges$Delta, freq=FALSE)
# lines(density(revdate_ranges$Delta))
# 
# est = fitdist(x/max(x), "beta", method="mme")
# est
# fitdist(x/max(x), probs=list(shape1=0.5, shape2=0.5), "beta", method="qme", start=est[[1]])
# fitdist(x/max(x), "beta", method="mle", start=est[[1]])
# 


y=revdate_ranges[revdate_ranges$Count>=2,][[3]]/(24*60*60)
x=revdate_ranges[revdate_ranges$Count>=2,][[2]]

linecolor=rgb(1,0,0)
svg(filename="date_v_size.svg", width=col_width, height=height, 
    family="Latin Modern Roman", pointsize=8)
mypar(c(1,1))
par(mar=c(2.75,3.0,1,1)+0.0)
plot(x, y, 
  type="p",
  main="", ylab="", xlab="", 
  axes=FALSE, log="xy",
  xlim=c(1.75, max(x)+2),
  ylim=c(1/24, 365.25*4),
  col=rgb(0, 0, 0, 0.25),
  pch=c(3))
# lines(seq(1,  length(x)), d2, col=rgb(1,0,1))
axis(2, 
  at=c(1/24,1,7,30,365.25,365.25*4),
  labels=c("Hour", "Day", "Week", "Month", "Year", "4Y")
  )
axis(1)
title(ylab="Lifetime", line=2)
title(xlab="Bucket Size", line=1.75)

dev.off()

cor.test(x,y, method="pearson")
cor.test(x,y, method="spearman")


signals = read.csv("signals-filtered.csv")

svg(filename="signals.svg", width=col_width, height=height, 
    family="Latin Modern Roman", pointsize=8)
mypar(c(1,1))
par(mar=c(1.75,3.0,1.5,1)+0.0)
xx <- barplot(signals$Count,
# legend=signals$Signal, 
#   type="p",
  main="", ylab="", xlab="", 
  axes=FALSE, log="",
#   xlim=c(0.8, length(x)+1),
#   ylim=c(1/24, 365.25*4),
#   col=rgb(0, 0, 0, 0.5)
)
# lines(seq(1,  length(x)), d2, col=rgb(1,0,1))
text(x=xx, y=signals$Count, label=signals$Count, pos=3, xpd=NA)
axis(2)
axis(1, mgp=c(3,-0.25,0),
    at=seq(1,length(signals$Count))*1.2-0.6,
   labels=c("SYS", "XFSZ", "XCPU", "ILL", "FPE", "BUS", "TRAP", "ABRT", "SEGV"),
   cex.axis=0.75,
   lty=0
)
title(ylab="Crashes", line=2.0)
title(xlab="Signal", line=0.75)

40592-sum(signals$Count)

dev.off()


architectures = read.csv("architectures-filtered.csv")

svg(filename="architectures.svg", width=col_width, height=height, 
    family="Latin Modern Roman", pointsize=10)
mypar(c(1,1))
par(mar=c(1.75,3.0,1.5,1)+0.0)
xx <- barplot(architectures$Count,
# legend=architectures$Signal, 
#   type="p",
  main="", ylab="", xlab="", 
  axes=FALSE, log="",
#   xlim=c(0.8, length(x)+1),
#   ylim=c(1/24, 365.25*4),
#   col=rgb(0, 0, 0, 0.5)
)
# lines(seq(1,  length(x)), d2, col=rgb(1,0,1))
text(x=xx, y=architectures$Count, label=architectures$Count, pos=3, cex=0.7, xpd=NA)
axis(2)
axis(1, mgp=c(3,-0.25,0),
    at=seq(1,length(architectures$Count))*1.2-0.6,
   labels=architectures$Architecture,
   cex.axis=0.75,
   lty=0
)
title(ylab="Crashes", line=2.0)
title(xlab="Architecture", line=0.75)

40592-sum(architectures$Count)

dev.off()



length(buckets$Count[buckets$Count==2])
length(buckets$Count[buckets$Count==1])


library(fitdistrplus)
library(logspline)

reclengths = read.csv("../recursion_results/length.csv")
sum(reclengths$count)
reclengths_filtered = reclengths[reclengths$length < 20,]
expanded = reclengths[rep(row.names(reclengths_filtered), reclengths_filtered$count), 1]-2

lengthmax = max(reclengths$length)

x = reclengths$length
# xgap <- ifelse(x > 40, x-2000+50, x)

svg(filename="reclengths.svg", width=col_width, height=height*1.33, 
    family="Latin Modern Roman", pointsize=8)
mypar(c(2,1))

par(mar=c(2.75,3.0,1,1)+0.0)
plot(x, reclengths$count, 
  type="h",
  main="", ylab="", xlab="", 
  axes=FALSE, log="y",
    xlim=c(-10, lengthmax),
   ylim=c(0.75, max(reclengths$count)+5000)
  )
library(plotrix)
axis(2, 
  at=c(1,10,100,1000,10000,max(reclengths$count)),
  labels=c(1,10,100,1000,NA,max(reclengths$count))) 
axis(1, 
    at=c(2,500,1000,1500,2000),
#   labels=c(0,10,20,30,1990,2000)
  )
title(ylab="Instances of Recursion", line=2.0)
title(xlab="Recursion Length", line=1.75)


par(mar=c(2.75,3.0,1,1)+0.0)
plot(x, reclengths$count, 
  type="h",
  main="", ylab="", xlab="", 
  axes=FALSE, log="y",
    xlim=c(1, 30),
   ylim=c(0.75, max(reclengths$count)+5000)
  )
library(plotrix)
axis(2, xpd=NA,
  at=c(1,10,100,1000,10000,max(reclengths$count)),
  labels=c(1,10,100,1000,NA,max(reclengths$count))) 
axis(1, 
    at=c(2,5,10,15,20,25,30),
#   labels=c(0,10,20,30,1990,2000)
  )
# axis.break(1,40,style="slash")
poisparm = fitdist(expanded, "pois", method="mle")
poisparm
poisfit = dpois(seq(0, 2000), poisparm[[1]][[1]]) * sum(reclengths$count)
geomparm = fitdist(expanded, "geom", method="mle")
geomparm
geomfit = dgeom(seq(0, 2000), geomparm[[1]][[1]]) * sum(reclengths$count)
nbinomparm = fitdist(expanded, "nbinom", method="mle")
nbinomparm
gofstat(nbinomparm)
nbinomfit = dnbinom(seq(0, 2000), size=nbinomparm[[1]][[2]], mu=nbinomparm[[1]][[2]]) * sum(reclengths$count)
# lines(seq(0,  2000)+2, poisfit, col=linecolor, cex=linesx)
lines(seq(0,  2000)+2, nbinomfit, col=linecolor)
# lines(seq(0,  2000)+2, geomfit, col=rgb(0,1,0), cex=linesx)
legend("topright", 
        legend=c(
#               "Poisson Distribution",
              "Negative Binomial Distribution"
#               "Geometric Distribution"
            ), col=c(
              linecolor
#               rgb(0,0,1),
#               rgb(0,1,0)
            ),
        lty=c(1),
        bty="n")

title(ylab="Crashes", line=2.0)
title(xlab="Recursion Length", line=1.75)

dev.off()


# descdist(expanded, discrete=TRUE)

stacklengths = read.csv("../recursion_results/stack_length.csv")
stacklengths_filtered = stacklengths[stacklengths$stack_length < 50,]
expanded = stacklengths[rep(row.names(stacklengths_filtered), stacklengths_filtered$count), 1]-1

lengthmax = max(stacklengths$count)

svg(filename="stacklengths.svg", width=col_width, height=height, 
    family="Latin Modern Roman", pointsize=8)
mypar(c(1,1))
par(mar=c(2.75,3.0,1,1)+0.0)
plot(stacklengths$stack_length, stacklengths$count, 
  type="h",
  main="", ylab="", xlab="", 
  axes=FALSE, log="xy",
   xlim=c(0.9, 2654),
   ylim=c(0.8, lengthmax)
  )
axis(2, at=c(1, 5, 10, 50, 100, 500, 1000, 2207)) 
axis(1, at=c(1, 10, 100, 1000, 2654))
poisparm = fitdist(expanded, "pois", method="mle")
poisparm
poisfit = dpois(seq(0, 2000), poisparm[[1]][[1]]) * sum(stacklengths$count)
geomparm = fitdist(expanded, "geom", method="mle")
geomparm
gofstat(geomparm)
geomfit = dgeom(seq(0, 2000), geomparm[[1]][[1]]) * sum(stacklengths$count)
nbinomparm = fitdist(expanded, "nbinom", method="mle")
nbinomparm
nbinomfit = dnbinom(seq(0, 2000), size=nbinomparm[[1]][[2]], mu=nbinomparm[[1]][[2]]) * sum(stacklengths$count)
# lines(seq(0,  2000)+2, poisfit, col=linecolor, cex=linesx)
# lines(seq(0,  2000)+2, nbinomfit, col=rgb(0,0,1), cex=linesx)
lines(seq(0,  2000)+2, geomfit, col=linecolor, cex=linesx)
title(ylab="Crashes", line=2.0)
title(xlab="Stack Length", line=1.75)
legend("topright", legend=c("Geometric Distribution"), col=c(linecolor),
        lty=c(1),
        bty="n")

dev.off()



fnlengths = read.csv("lengths.csv")
lengthmax = max(tabulate(fnlengths$Length))
countslen = max(fnlengths$Length)
svg(filename="fnlengths.svg", width=col_width, height=height*1.33, 
    family="Latin Modern Roman", pointsize=8)
mypar(c(2,1))
par(mar=c(2.75,3.0,1,1)+0.0)
plot(seq(1,countslen), tabulate(fnlengths$Length),
  type="h",
  main="", ylab="", xlab="", 
  axes=FALSE, log="xy",
   xlim=c(0.8, countslen),
   ylim=c(0.5, lengthmax+100000)
  )
# lines(seq(1,  length(x)), d2, col=rgb(1,0,1))
# text(x=xx, y=architectures$Count, label=architectures$Count, pos=3, cex=mex*0.7)
axis(2, at=c(1, 10, 100, 1000, 10000, lengthmax)) 
axis(1, at=c(1, 10, 100, countslen ))
lens = fnlengths$Length
lensf = fnlengths$Length[fnlengths$Length > 0]
# lens = lens[lens!=0]-1
# poisparm = fitdist(lens, "pois", method="mle")
# poisparm
# poisfit = dpois(seq(0, 100), poisparm[[1]][[1]]) * sum(table(lens))
# geomparm = fitdist(fnlengths$Length, "geom", method="mle")
# geomparm
# geomfit = dgeom(seq(0, 100), geomparm[[1]][[1]]) * sum(table(lens))
# nbinomparm = fitdist(lens, "nbinom", method="mle")
# nbinomparm
# nbinomfit = dnbinom(seq(0, 100), size=nbinomparm[[1]][[2]], mu=nbinomparm[[1]][[2]]) * sum(table(lens))
gammaparm = fitdist(lensf, "gamma", method="mme")
gammaparm = fitdist(lensf, "gamma", method="qme", probs=gammaparm[[1]])
gammaparm
gofstat(gammaparm)
ks.test(x, pgamma,  gammaparm[[1]][[1]], gammaparm[[1]][[2]])
gammafit = dgamma(seq(0, 100), gammaparm[[1]][[1]], gammaparm[[1]][[2]]) * sum(table(lensf))
lines(seq(0,  100), gammafit, col=linecolor)
# lines(seq(0,  100), nbinomfit, col=rgb(0,0,1), cex=linesx)
# lines(seq(0,  100), geomfit, col=rgb(0,1,0), cex=linesx)
# lines(seq(0,  100), poisfit, col=linecolor, cex=linesx)
legend("topright", legend=c("Gamma Distribution"), col=c(linecolor),
        lty=c(1),
        bty="n")
title(ylab="Number of Frames", line=2.0)
title(xlab="Function Name Length in Tokens", line=1.75)
# =======================
ufnlengths = read.csv("unique_lengths.csv")
lengthmax = max(tabulate(ufnlengths$Length))
countslen = max(ufnlengths$Length)
par(mar=c(2.75,3.0,1,1)+0.0)
plot(seq(1,countslen), tabulate(ufnlengths$Length),
  type="h",
  main="", ylab="", xlab="", 
  axes=FALSE, log="xy",
   xlim=c(0.8, countslen),
   ylim=c(0.5, lengthmax+3000)
  )
# lines(seq(1,  length(x)), d2, col=rgb(1,0,1))
# text(x=xx, y=architectures$Count, label=architectures$Count, pos=3, cex=mex*0.7)
axis(2, at=c(1, 10, 100, 1000, lengthmax)) 
axis(1, at=c(1, 10, 100, countslen ))
lens = ufnlengths$Length
# lens = lens[lens!=0]-1
# poisparm = fitdist(lens, "pois", method="mle")
# poisparm
# poisfit = dpois(seq(0, 100), poisparm[[1]][[1]]) * sum(table(lens))
gammaparm = fitdist(lens, "gamma", method="mme")
gammaparm = fitdist(lens, "gamma", method="qme", probs=gammaparm[[1]])
gammaparm
gofstat(gammaparm)
ks.test(x, pgamma,  gammaparm[[1]][[1]], gammaparm[[1]][[2]])
gammafit = dgamma(seq(0, 100), gammaparm[[1]][[1]], gammaparm[[1]][[2]]) * sum(table(lens))

# geomparm = fitdist(lens, "geom", method="mle")
# geomparm
# geomfit = dgeom(seq(0, 100), geomparm[[1]][[1]]) * sum(table(lens))
# nbinomparm = fitdist(lens, "nbinom", method="mle")
# nbinomparm
# nbinomfit = dnbinom(seq(0, 100), size=nbinomparm[[1]][[2]], mu=nbinomparm[[1]][[2]]) * sum(table(lens))
# lines(seq(0,  100), nbinomfit, col=rgb(0,0,1), cex=linesx)
# lines(seq(0,  100), paretofit, col=rgb(0,1,0), cex=linesx)
lines(seq(0,  100), gammafit, col=linecolor, cex=linesx)
legend("topright", legend=c("Gamma Distribution"), col=c(linecolor),
        lty=c(1),
        bty="n")
title(ylab="Number of Unique Function Names", line=2.0)
title(xlab="Function Name Length in Tokens", line=1.75)
dev.off()
