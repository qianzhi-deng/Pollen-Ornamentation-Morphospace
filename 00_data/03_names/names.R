suppressMessages(library(rWCVP))

HERE <- dirname(sub("--file=", "", commandArgs(FALSE)[grep("--file=", commandArgs(FALSE))]))
species <- unique(c(read.csv(file.path(HERE, "..", "01_pollen", "metadata.csv"))$species,
                    read.csv(file.path(HERE, "..", "02_pollination", "pollination.csv"))$species))
wcvp <- rWCVPdata::wcvp_names

matched <- wcvp_match_names(data.frame(species = species, query = sub(" ssp\\. (\\S+)", " subsp. \\L\\1", species, perl = TRUE)),
                            name_col = "query", fuzzy = FALSE)
matched <- matched[matched$wcvp_status %in% c("Accepted", "Synonym"), ]
matched <- matched[order(matched$wcvp_status != "Accepted"), ]
matched <- matched[!duplicated(matched$species), ]
accepted <- match(matched$wcvp_accepted_id, wcvp$plant_name_id)
infra <- wcvp$taxon_rank[accepted] != "Species"
accepted[infra] <- match(wcvp$parent_plant_name_id[accepted[infra]], wcvp$plant_name_id)
write.csv(data.frame(species = matched$species, accepted = wcvp$taxon_name[accepted],
                     genus = wcvp$genus[accepted], family = wcvp$family[accepted]),
          file.path(HERE, "names.csv"), row.names = FALSE)
