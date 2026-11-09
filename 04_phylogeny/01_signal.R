suppressMessages({library(ape); library(caper)})

HERE <- dirname(sub("--file=", "", commandArgs(FALSE)[grep("--file=", commandArgs(FALSE))]))
tree <- read.tree(file.path(HERE, "..", "00_data", "04_tree", "tree.nwk"))
tree$node.label <- NULL
data <- comparative.data(tree, subset(read.csv(file.path(HERE, "..", "03_function", "species.csv")), family == "Asteraceae"), tip)

signal <- do.call(rbind, lapply(c("I", "D", "P"), function(axis) {
  ci <- pgls.confint(pgls(reformulate("1", axis), data, lambda = "ML"), "lambda")
  lim <- ifelse(is.na(ci$ci.val), ci$bounds.val, ci$ci.val)
  data.frame(axis = axis, lambda = ci$opt[[1]], lo = lim[1], hi = lim[2], lambda_p = ci$bounds.p[1])
}))
signal$lambda_p_fdr <- p.adjust(signal$lambda_p, "BH")
signal[-1] <- round(signal[-1], 4)
write.csv(signal, file.path(HERE, "signal.csv"), row.names = FALSE)
