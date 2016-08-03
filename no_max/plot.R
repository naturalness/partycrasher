#!/usr/bin/env python

#  Copyright (C) 2016 Joshua Charles Campbell

#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

allcolors <- c(rgb(0.5, 0.5, 0), rgb(0.5, 0.5, 0.5), rgb(0.5, 0, 0), rgb(0, 0.5, 0.5))
colors <- rep(allcolors[1:4], each=1, times=2)
fcolors <- rep(allcolors[5:7], times=6)
linetype <- rep(c(1,2), each=10)
plotchar <- rep(c(22, 21, 24, 23, 25), 10)

shrink = 3
mex = shrink/1.255
linesx = 2.0
# 
plota<-function(x, data, y, xlim, ylim, lnames, lpos) {
    par(mar=c(1.75,2.0,0.75,0)+0.0)
    plot(x[[1]], data[[1]], type='n', 
        ylab="", xlab="", axes=FALSE,
        xlim=xlim, ylim=ylim)
    axis(2, mgp=c(1.25, 0.25, 0), lwd=(1/shrink)) 
    axis(1, mgp=c(1.5, 0.5, 0), lwd=(1/shrink))
    title(ylab=y, line=1.0)
    title(xlab="Crashes Seen", line=1.25)
    i = 1
#     lines(x, data, type='o', cex=linesx,
#     lty=linetype[i], col=colors[i], pch=plotchar[i], bg=fcolors[i])
#     lnames=mnames
    nmethods=length(data)
    for (i in 1:nmethods) {
        method <- data[[i]]
        lines(x[[i]], method, type='o', cex=linesx,
        lty=linetype[i], col=colors[i], pch=NA, bg=fcolors[i])
    }
#     if (!is.null(oracle)) {
#         i = nmethods+1
#         print(i)
#         method <- data[[1]]
#         lnames=c(lnames, oracle)
#         lines(method[["n"]], method[["obuckets"]], type='o', cex=linesx,
#         lty=linetype[i], col=colors[i], pch=plotchar[i], bg=fcolors[i])
#     }
    if (length(lnames)>0) {
#         par(family="Latin Modern Mono")
        legend(lpos, legend=lnames, col=colors, pch=plotchar, lty=linetype,
            title="Method", cex=mex*0.9, pt.cex=linesx, bty="n", ncol=1,
            pt.bg=fcolors,
            xjust=0
            )
        par(family="Latin Modern Roman")
    }
}

plotablines<-function(models) {
    nmodels=length(models)
    for (i in 1:nmodels) {
        abline(models[[i]],
              cex=linesx,
              lty=linetype[i], col=colors[i], bg=fcolors[i])
    }
}


mypar <- function(mfrow) {
par(
    mfrow=mfrow,
    cex=(1/shrink),
    cex.axis=mex,
    cex.lab=mex,
    cex.main=mex,
    cex.sub=mex,
    mex=mex,
    lwd=(1/shrink),
    oma=c(0,0,0,0),
    xpd=FALSE,
    tcl=0.5,
    xaxs="i",
    yaxs="i",
    bty="n"
    )
}

library(MASS)

page_width=7.15
width=page_width
height=(page_width/3)
svg(filename="no_max.svg", width=page_width, height=height, 
    family="Latin Modern Roman", pointsize=10)
mypar(c(1,2))
nomax = read.csv("T4.0.csv")
nomax$time = nomax$time/1000
mysol = read.csv("../auto_max_query_terms/T4.0.csv")
mysol1 = read.csv("../min1/T4.0.csv")
normless = read.csv("../T4.0.csv")
mysol$time = mysol$time/1000
mysol1$time = mysol1$time/1000
normless$time = normless$time/1000
modelnomax = rlm(nomax$time ~ nomax$after)
modelmysol = rlm(mysol$time ~ mysol$after)
modelmysol1 = rlm(mysol1$time ~ mysol1$after)
xlim = c(0, 225000)
# print(modelnomax)
lnames = list("Fixed MQT", "Auto MQT", "Auto MQT min_score=1")
print(summary(modelmysol)$coefficients)
plota(list(nomax$after, mysol$after, mysol1$after, normless$after), 
      list(nomax$time, mysol$time, mysol1$time, normless$time), "Time Per Crash", 
      xlim=xlim, ylim=c(0,0.4),
      lnames,
      lpos="topleft")
plotablines(list(modelnomax, modelmysol, modelmysol1))

modelnomax = rlm(nomax$b3f ~ nomax$after)
modelmysol = rlm(mysol$b3f ~ mysol$after)
modelmysol1 = rlm(mysol1$b3f ~ mysol1$after)
# print(modelnomax)
# print(modelmysol)

plota(list(nomax$after, mysol$after, mysol1$after, normless$after), 
      list(nomax$b3f, mysol$b3f, mysol1$b3f, normless$b3f), "F-Score @ T=4.0", 
      xlim=xlim, ylim=c(0.7,1.0),
      lnames,
      lpos="topleft")
plotablines(list(modelnomax, modelmysol, modelmysol1))
dev.off()

