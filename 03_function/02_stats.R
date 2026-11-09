suppressMessages({library(ape); library(nlme); library(effsize)})

HERE <- dirname(sub("--file=", "", commandArgs(FALSE)[grep("--file=", commandArgs(FALSE))]))
species <- read.csv(file.path(HERE, "species.csv"))
species$vector <- factor(species$vector, c("wind", "insect"))
species <- species[!is.na(species$vector), ]
tree <- keep.tip(read.tree(file.path(HERE, "..", "00_data", "04_tree", "tree.nwk")), species$tip)

stats <- do.call(rbind, lapply(c("I", "D", "P"), function(axis) {
  y <- split(species[[axis]], species$vector)
  fit <- gls(reformulate("vector", axis), species, corPagel(1, tree, form = ~tip), method = "ML")
  est <- summary(fit)$tTable["vectorinsect", ]
  ci <- intervals(fit, which = "coef")$coef["vectorinsect", ]
  data.frame(axis = axis, n_insect = length(y$insect), n_wind = length(y$wind),
             cohen_d = cohen.d(y$insect, y$wind)$estimate,
             pgls_diff = est[["Value"]], pgls_se = est[["Std.Error"]], pgls_df = fit$dims$N - fit$dims$p,
             ci_lo = ci[["lower"]], ci_hi = ci[["upper"]], pgls_p = est[["p-value"]],
             lambda = coef(fit$modelStruct$corStruct, unconstrained = FALSE)[[1]])
}))
stats$pgls_p_fdr <- p.adjust(stats$pgls_p, "BH")
stats[-1] <- round(stats[-1], 4)
write.csv(stats, file.path(HERE, "stats.csv"), row.names = FALSE)
