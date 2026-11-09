suppressMessages({library(ape); library(caper); library(phytools)})

HERE <- dirname(sub("--file=", "", commandArgs(FALSE)[grep("--file=", commandArgs(FALSE))]))
tree <- read.tree(file.path(HERE, "..", "00_data", "04_tree", "tree.nwk"))
tree$node.label <- NULL
data <- comparative.data(tree, subset(read.csv(file.path(HERE, "..", "03_function", "species.csv")), family == "Asteraceae"), tip)

phy <- data$phy
nodes <- 1:(Ntip(phy) + phy$Nnode)
write.csv(data.frame(node = nodes, parent = phy$edge[match(nodes, phy$edge[, 2]), 1],
                     sapply(c(I = "I", D = "D", P = "P"), function(axis) c(data$data[[axis]], fastAnc(phy, setNames(data$data[[axis]], phy$tip.label)))),
                     is_tip = as.integer(nodes <= Ntip(phy)), label = c(phy$tip.label, rep("", phy$Nnode))),
          file.path(HERE, "ancestral.csv"), row.names = FALSE)
