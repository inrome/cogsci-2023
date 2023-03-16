library(tidyverse)
library(openxlsx)

ts_raw <- read.xlsx("prolific_data/n_97_openlab_full_data.xlsx")

ts_raw %>% distinct(openLabId) %>% count()
ts_raw %>% distinct(code) %>% count()

# generate unique IDs
ids <- ts_raw %>% distinct(code, openLabId) %>% mutate(participant_id = 1:nrow(.))
n <- nrow(ids)
filename <- paste0("outputs/", format(Sys.Date(),"%Y-%m-%d"), "_removed-ids", "_an-exp1_n-",n, ".csv")
write.csv(ids, filename, row.names = F) # write them in a csv just in case

# substitude Prolific ID with new code in trials 
ts_anonym <- ts_raw %>% left_join(ids) %>% select(-code, -openLabId)
n <- ts_anonym %>% distinct(participant_id) %>% nrow
filename <- paste0("outputs/", format(Sys.Date(),"%Y-%m-%d"),"_","trials_anonymized", "_","an-exp1_n-",n, ".csv")
write.csv(ts_anonym, filename, row.names = F) # write them in a csv just in case

# Get Prolific meta data
tmp_prolific <- read.csv("prolific_data/n_97 prolific demographics part_2.csv")
tmp_prolific <- tmp_prolific %>% rename(code = Participant.id) %>% mutate(Age = as.integer(Age))

# for old prolific data
tmp_prolific2 <- read.csv("prolific_data/n_12_2023-01-23_meta.csv") 
tmp_prolific2 <- tmp_prolific2 %>% rename(code = Participant.id)

# combine them together
tmp_prolific <- tmp_prolific2 %>% bind_rows(tmp_prolific) %>% select(-Completion.code, -Status, -Submission.id)

tmp_prolific_anonym <- tmp_prolific %>% left_join(ids) %>% select(-code)
n <- tmp_prolific_anonym %>% distinct(participant_id) %>% nrow
filename <- paste0("outputs/", format(Sys.Date(),"%Y-%m-%d"),"_","demographics_anonymized", "_","an-exp1_n-",n, ".csv")
write.csv(tmp_prolific_anonym, filename, row.names = F) # write them in a csv just in case
