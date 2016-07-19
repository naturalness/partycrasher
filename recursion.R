#!/usr/bin/env Rscript

library(plyr)
library(ggplot2)

rec <- read.csv("recursion.csv")
rec.total <- count(rec, 'max.depth')

print(rec.total)

ggplot(rec.total, aes(max.depth)) + geom_bar()

summary(rec)
var(rec)
