# Load the required libraries
library("bayesAB")
library("tidyverse")
library("dampack")




df <- read.csv("data_experiment.csv")


df1 <- data.frame(df)
df1$group <- ifelse(df1$group == "treatment", "test", df1$group)
df1[c("visits", "clicks")] <- lapply(df1[c("visits", "clicks")], as.integer)



control <- rbinom(150, 1, .20)
treatment <- rbinom(150, 1, .235)

plotBeta(60, 200)



full_base = c(control,treatment)


alpha <- beta_params(mean(full_base), sd(full_base))$alpha
beta <- beta_params(mean(full_base), sd(full_base))$beta


alpha

AB1 <- bayesTest(control, treatment, priors = c('alpha' = 60, 'beta' = 200), n_samples = 1e5, distribution = 'bernoulli')



summary(AB1)

