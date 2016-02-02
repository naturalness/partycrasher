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

top1 = read.csv("top1.csv")
methods <- c(
            "top1.csv", 
            "top2.csv",  
            "top3.csv",
            "top1a.csv", 
            "top1f.csv",
            "top1m.csv", 
            "lerch4.0.csv", 
            "lerchc.csv",
            "cc.csv"
            )
mnames <- c(
            "1Frame", 
            "2Frame",  
            "3Frame",
            "1Addr", 
            "1File",
            "1Mod", 
            "Lerch", 
            "LerchC",
            "CamelC"
            )
data = NULL
data = lapply(setNames(methods, make.names(mnames)), 
         read.csv)
allcolors <- gray.colors(7, start=0.0, end=1.0)
colors <- rep(allcolors[1:3], each=3)
fcolors <- rep(allcolors[5:7], times=3)
linetype <- rep(c(1,2), each=10)
plotchar <- rep(c(22, 21, 24, 23, 25), 10)

shrink = 3
mex = shrink/1.255
linesx = 2.0

plota<-function(data, metric, y, l, ylim=c(0.2,1.0), lpos="bottomleft",
                oracle=NULL){
    par(mar=c(1.75,2.0,0.75,0)+0.0)
    plot(top1$n, top1$b3f, type='n', ylim=ylim, xlim=c(0,16000),
        ylab="", xlab="", axes=FALSE)
    axis(2, mgp=c(1.25, 0.25, 0), lwd=(1/shrink)) 
    axis(1, mgp=c(1.5, 0.5, 0), lwd=(1/shrink))
    title(ylab=y, line=1.0)
    title(xlab="Crashes Seen", line=1.25)
    lnames=mnames
    nmethods=length(data)
    for (i in 1:nmethods) {
        method <- data[[i]]
        lines(method[["n"]], method[[metric]], type='o', cex=linesx,
        lty=linetype[i], col=colors[i], pch=plotchar[i], bg=fcolors[i])
    }
    if (!is.null(oracle)) {
        i = nmethods+1
        method <- data[[1]]
        lnames=c(lnames, oracle)
        lines(method[["n"]], method[["obuckets"]], type='o', cex=linesx,
        lty=linetype[i], col=colors[i], pch=plotchar[i], bg=fcolors[i])
    }
    if (l) {
        par(family="Latin Modern Mono")
        legend(lpos, legend=lnames, col=colors, pch=plotchar, lty=linetype,
            title="Method", cex=mex*0.9, pt.cex=linesx, bty="n", ncol=3,
            pt.bg=fcolors,
            xjust=0
            )
        par(family="Latin Modern Roman")
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
    xpd=NA,
    tcl=0.5,
    xaxs="i",
    yaxs="i",
    bty="n"
    )
}
page_width=7.15
width=page_width
height=(page_width/3)
svg(filename="b3.svg", width=page_width, height=height, 
    family="Latin Modern Roman", pointsize=10)
mypar(c(1,3))
plota(data, "b3p", "BCubed Precision", l=TRUE)
plota(data, "b3r", "BCubed Recall", l=FALSE)
plota(data, "b3f", "BCubed F1-Score", l=FALSE)
dev.off()
svg(filename="pur.svg", width=page_width, height=(width/3), 
    family="Latin Modern Roman", pointsize=10)
mypar(c(1,3))
plota(data, "purity", "Purity", l=TRUE)
plota(data, "invpur", "Inverse Purity", l=FALSE)
plota(data, "purf", "Purity F1-Score", l=FALSE)
dev.off()

col_width=3.5
width=col_width
svg(filename="nbuckets.svg", width=col_width, height=height, 
    family="Latin Modern Roman", pointsize=10)
mypar(c(1,1))
plota(data, "buckets", "Total Number of Buckets Created", l=TRUE, ylim=c(0,14400), 
    lpos="topleft", oracle="Ubuntu")
dev.off()

vals <- c("2.0", "3.0",
          "4.0", "4.5",
          "5.0", "6.0", "8.0", "10.0")

methods <- lapply(vals, function(i){paste0("mlts",i,".csv")})
mnames <- lapply(vals, function(i){paste0("T=",i)})
data = NULL
data = lapply(setNames(methods, make.names(mnames)), 
         read.csv)
            
svg(filename="b3t.svg", width=page_width, height=height, 
    family="Latin Modern Roman", pointsize=10)
mypar(c(1,3))
plota(data, "b3p", "BCubed Precision", l=FALSE)
plota(data, "b3r", "BCubed Recall", l=TRUE, lpos="topleft")
plota(data, "b3f", "BCubed F1-Score", l=FALSE)
dev.off()
svg(filename="purt.svg", width=page_width, height=height, 
    family="Latin Modern Roman", pointsize=10)
mypar(c(1,3))
plota(data, "purity", "Purity", l=FALSE)
plota(data, "invpur", "Inverse Purity", l=TRUE, lpos="topleft")
plota(data, "purf", "Purity F1-Score", l=FALSE)
dev.off()
svg(filename="nbucketst.svg", width=col_width, height=height, 
    family="Latin Modern Roman", pointsize=10)
mypar(c(1,1))
plota(data, "buckets", "Total Number of Buckets Created", l=TRUE, ylim=c(0,15000), 
    lpos="topleft", oracle="Ubuntu")
dev.off()


vals <- c("0.0", 
#           "0.25",
          "0.5", "1.0", "1.5",
          "2.0", "2.25", "2.5", "2.75", "3.0", "3.25", "3.5", "3.75",
          "4.0", "4.5", "5.0", "5.5", "6.0", "7.0", "8.0", "10.0")

methods <- lapply(vals, function(i){paste0("mlts",i,".csv")})
mnames <- lapply(vals, function(i){paste0("T=",i)})
data = NULL
data = lapply(setNames(methods, make.names(mnames)), 
         read.csv)

p = lapply(1:length(data), function(ti){tail(data[[ti]][["b3p"]],n=1)})
r = lapply(1:length(data), function(ti){tail(data[[ti]][["b3r"]],n=1)})
f = lapply(1:length(data), function(ti){tail(data[[ti]][["b3f"]],n=1)})
t = lapply(1:length(data), function(ti){paste0(" ", mnames[ti], " F=.",
                                               sprintf("%02i ", round(100*f[[ti]])))
                                        })
svg(filename="prc.svg", width=col_width, height=col_width, 
    family="Latin Modern Roman", pointsize=10)
mypar(c(1,1))
par(mar=c(1.75,2.0,1.75,0)+0.0)
plot(p, r, xlim=c(0,1.01), ylim=c(0,1), asp=1,
        ylab="", xlab="", axes=FALSE,
        pch=19, cex=linesx)
axis(2, mgp=c(1.5, 0.5, 0), lwd=(1/shrink), pos=0) 
axis(1, mgp=c(1.5, 0.5, 0), lwd=(1/shrink), pos=0)
px = c(0, p, tail(p,n=1), 0)
rx = c(head(r,n=1),r, 0, 0)
polygon(px, rx, border=NA, col="#0000003f")
reorientate = (1:length(p))[p<0.5]
text(p[reorientate], r[reorientate], labels=t[reorientate],
     adj=c(0,0.5), cex=mex, srt=15)
text(p[-(reorientate)], r[-(reorientate)], labels=t[-(reorientate)],
     adj=c(1,0.5), cex=mex, srt=15)
title(ylab="BCubed Recall", line=1.0)
title(xlab="BCubed Precision", line=1.25)
dev.off()


methods <- c(
            "ccs.csv",  
            "cc.csv", 
#             "let.csv",
#             "letl.csv", 
            "spcs.csv", 
            "spc.csv", 
#             "spcl.csv",
#             "uni.csv", 
#             "unil.csv",
#             "id.csv",
#             "idl.csv",
#             "ids.csv",
#             "idls.csv",
            "lerch4.0.csv",
            "lerchc.csv"
            )
mnames <- c(
             "Camel",  
             "CamelC", 
#             "Lett",
#             "lettc", 
            "Space",
            "SpaceC", 
#             "Uni", 
#             "unic",
#             "IdC",
#             "idc",
#             "Id",
#             "id",
            "Lerch",
            "LerchC"
            )
data = NULL
data = lapply(setNames(methods, make.names(mnames)), 
         read.csv)
svg(filename="b3a.svg", width=page_width, height=height, 
    family="Latin Modern Roman", pointsize=10)
mypar(c(1,3))
plota(data, "b3p", "BCubed Precision", l=FALSE, ylim=c(0.2, 1.0))
plota(data, "b3r", "BCubed Recall", l=TRUE, lpos="topleft", ylim=c(0.2, 1.0))
plota(data, "b3f", "BCubed F1-Score", l=FALSE, ylim=c(0.2, 1.0))
dev.off()
svg(filename="pura.svg", width=page_width, height=height, 
    family="Latin Modern Roman", pointsize=10)
mypar(c(1,3))
plota(data, "purity", "Purity", l=FALSE, ylim=c(0.55, 0.925))
plota(data, "invpur", "Inverse Purity", l=TRUE, lpos="topleft", ylim=c(0.55, 0.925))
plota(data, "purf", "Purity F1-Score", l=FALSE, ylim=c(0.55, 0.925))
dev.off()
svg(filename="nbucketsa.svg", width=col_width, height=height, 
    family="Latin Modern Roman", pointsize=10)
mypar(c(1,1))
plota(data, "buckets", "Total Number of Buckets Created", l=TRUE, ylim=c(0,14400), 
    lpos="topleft", oracle="Oracle")
dev.off()
