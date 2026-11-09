suppressMessages(library(V.PhyloMaker2))

HERE <- dirname(sub("--file=", "", commandArgs(FALSE)[grep("--file=", commandArgs(FALSE))]))
angiosperms <- with(read.csv(file.path(HERE, "..", "01_pollen", "metadata.csv")), species[seed_group == "Angiosperm"])
taxa <- read.csv(file.path(HERE, "..", "03_names", "names.csv"))

taxa <- taxa[taxa$species %in% angiosperms & taxa$genus %in% sub("_.*", "", GBOTB.extended.TPL$tip.label), ]
tree <- phylo.maker(data.frame(species = taxa$accepted, genus = taxa$genus, family = taxa$family))$scenario.3
ape::write.tree(tree, file.path(HERE, "tree.nwk"))
