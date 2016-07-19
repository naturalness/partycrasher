#!/usr/bin/env Rscript

library(plyr)
library(ggplot2)

rec <- read.csv("recursion.csv")
rec.total <- count(rec, 'max.depth')

print(rec.total)

ggplot(rec.total, aes(max.depth)) + geom_bar()

summary(rec)
var(rec)
library(MASS)

# estimate mu and theta (aka size) based on mean/variance
# from http://stats.stackexchange.com/questions/143977/choosing-reasonable-parameters-for-a-negative-binomial-distribution
mu_start = mean(rec$max.depth)
theta_start = (mu_start**2)/(var(rec$max.depth)-mu_start)


params <- fitdistr(rec$max.depth, "Negative Binomial",
      list(size=theta_start, mu=mu_start), lower=0.00001 )

# # try making fake data!
# fake <- rnegbin(20000, mu=params$estimate['mu'], theta=params$estimate['size'])
# fake.total <- count(fake)
# print(fake.total)
# 
# fake <- rnegbin(20000, mu=mu_start, theta=theta_start)
# fake.total <- count(fake)
# print(fake.total)
