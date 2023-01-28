library(tidyverse)


# load data 
ts_raw <- read.csv("outputs/2023-01-28_trials_anonymized_an-exp1_n-97.csv")

# Learning phase ####
ts_learning <- ts_raw %>% select(participant_id, fsm_number, trial_number, state_current, response_current, state_next, 
                  state_1, response_1, state_2, response_2, state_3, 
                  response, duration, sender) %>% 
  filter(sender %in% c("respose_1_screen", "respose_2_screen","response_further_screen", "further_trials_seq", "first_five_trials_seq"))  %>% 
  mutate(response_time = dplyr::lag(duration)) %>%  # add correct response times 
  filter(trial_number >= 1) %>% select(-duration, -sender, -response) %>%  # fix second trials
  mutate(state_1 = ifelse(trial_number == 2, lag(state_current), state_1), 
         response_1 = ifelse(trial_number == 2, lag(response_current), response_1), 
         state_2 = ifelse(trial_number == 2, state_current, state_2), 
         response_2 = ifelse(trial_number == 2, response_current, response_2), 
         state_3 = ifelse(trial_number == 2, state_next, state_3)) %>% 
  mutate(state_1 = ifelse(trial_number == 1, NA, state_1), 
         response_1 = ifelse(trial_number == 1, NA, response_1), 
         state_2 = ifelse(trial_number == 1, NA, state_2), 
         response_2 = ifelse(trial_number == 1, NA, response_2), 
         state_3 = ifelse(trial_number == 1, NA, state_3)) %>% #fix first trials
  mutate(response_time_lessThan300ms = ifelse(response_time <= 300, 1, 0), 
         trial_id = paste0(state_current, response_current, state_next))

n <- nrow(ts_learning %>% group_by(participant_id) %>% count())
filename <- paste0("outputs/", format(Sys.Date(),"%Y-%m-%d"), "_learning", "_an-exp1_n-",n, ".csv")
write.csv(ts_learning, filename, row.names = F)


# Transitions (Mental Models) ####

# calculate frequencies and proportions of observed next states
tmp_transitions <- ts_learning %>% 
  group_by(participant_id, 
          state_current, 
          response_current, 
          state_next) %>% summarise(state_next_n = n()) %>% 
  group_by(participant_id, state_current, response_current) %>% 
  mutate(state_next_p = state_next_n / sum(state_next_n))


tmp_expanded <- ts_learning %>%  expand(participant_id, state_current, response_current, state_next)

transitions <- tmp_expanded %>% left_join(tmp_transitions) %>% 
  replace(is.na(.), 0)  %>%  ungroup() # replace all NA with 0 

n <- nrow(tmp_transitions %>% group_by(participant_id) %>% count())
filename <- paste0("outputs/", format(Sys.Date(),"%Y-%m-%d"), "_transitions", "_an-exp1_n-",n, ".csv")
write.csv(transitions, filename, row.names = F)

# Prediction #### 
ts_prediction <- ts_raw %>% filter(test_prediction_counter >=0 & 
                                     !(is.na(response))) %>% 
  select(participant_id, fsm_number, trial_number = test_prediction_counter, trial_type = exp_type, 
         state_1, response_1, state_2, response_2, option_1, option_2,
         prediction_correct, response, response_correct = correct,
         option_1_p, option_2_p) %>% mutate(fsm_type = ifelse(fsm_number == 21, "easy", "hard"), 
                                            trial_number = trial_number + 1, 
                                            trial_id = ifelse(trial_type == "visible", 
                                                              paste0(fsm_type,"_p_vis_", state_1, response_1, state_2, response_2, option_1, option_2), 
                                                              paste0(fsm_type,"_p_hid_", state_1, response_1, response_2, option_1, option_2))) %>% 
  select(participant_id,fsm_type,trial_number,trial_type, trial_id, state_1:option_2_p)

n <- nrow(ts_prediction %>% group_by(participant_id) %>% count())
filename <- paste0("outputs/", format(Sys.Date(),"%Y-%m-%d"), "_test_prediction_", "an-exp1_N-97-n-",n, ".csv")
write.csv(ts_prediction, filename, row.names = F)

# Control ####
ts_control<- ts_raw %>% filter(test_control_counter >=0 & 
                                     !(is.na(response))) %>% 
  select(participant_id, fsm_number, trial_number = test_control_counter, trial_type = exp_type, 
         state_1, response_1, state_2, state_3, option_1, option_2,
         control_correct, response, response_correct = correct,
         option_1_p, option_2_p) %>% mutate(fsm_type = ifelse(fsm_number == 21, "easy", "hard"), 
                                            response_1 = ifelse(response_1 == "", "NA", response_1),
                                            trial_id = ifelse(trial_type == "visible", 
                                                              paste0(fsm_type,"_c_vis_", state_1, response_1, state_3), 
                                                              paste0(fsm_type,"_c_hid_", state_1, state_3, "-", option_1,"-",option_2))) %>% 
  select(participant_id,fsm_type,trial_number,trial_type, trial_id, state_1:option_2_p)

n <- nrow(ts_control %>% group_by(participant_id) %>% count())
filename <- paste0("outputs/", format(Sys.Date(),"%Y-%m-%d"), "_test_control_", "an-exp1_N-97-n-",n, ".csv")
write.csv(ts_control, filename, row.names = F)

# Explanation ####
ts_explanation <- ts_raw %>% filter(test_explanation_counter >=0 & 
                                 !(is.na(response))) %>% 
  select(participant_id, fsm_number, trial_number = test_explanation_counter, trial_type = exp_type, 
         state_1, response_1, state_2, response_2, state_3, explanation_1_decrease, explanation_2_decrease,
         explanation_correct, response, response_correct = correct) %>% 
  mutate(fsm_type = ifelse(fsm_number == 21, "easy", "hard"),
         trial_id = ifelse(trial_type == "visible", 
                            paste0(fsm_type,"_e_vis_", state_1, response_1, state_2, response_2, state_3), 
                            paste0(fsm_type,"_e_hid_", state_1, response_1, response_2, state_3))) %>% 
  select(participant_id,fsm_type,trial_number,trial_type, trial_id, state_1:response_correct)

n <- nrow(ts_explanation %>% group_by(participant_id) %>% count())
filename <- paste0("outputs/", format(Sys.Date(),"%Y-%m-%d"), "_test_explanation_", "an-exp1_N-97-n-",n, ".csv")
write.csv(ts_explanation, filename, row.names = F)

# Participants ####
tmp_ss <- ts_raw %>% 
  select(participant_id, 
         study_task = test_condition, 
         study_fsm = fsm_number, 
         q_estimate, q_strategy = q_stategy_scale, 
         txt_advice = q_strategy,
         meta_timestamp = timestamp)

ss <- tmp_ss %>% group_by(participant_id) %>% 
  summarise(study_task = first(na.omit(study_task)), 
            study_fsm = first(na.omit(study_fsm)),
            meta_timestamp = first(na.omit(meta_timestamp)),
            q_strategy = first(na.omit(q_strategy)),
            q_estimate = first(na.omit(q_estimate)),
            meta_timestamp = first(na.omit(meta_timestamp))) %>% 
  left_join(tmp_ss %>% select(participant_id, txt_advice) %>% filter(!txt_advice == "")) %>% mutate(study_fsm = ifelse(study_fsm == 21, "easy", "hard"))

# Add Prolific demographic data
ss_demogr <- read.csv("outputs/2023-01-28_demographics_anonymized_an-exp1_n-97.csv") 
ss_demogr <- ss_demogr %>% select(participant_id, 
                                        subject_age = Age, subject_sex = Sex, 
                                        subject_ethnicity = Ethnicity.simplified, 
                                        subject_timeTaken = Time.taken)

ss <- ss %>% left_join(ss_demogr)
n <- nrow(ss)
filename <- paste0("outputs/", format(Sys.Date(),"%Y-%m-%d"), "_participants_", "an-exp1_N-",n,".csv")
write.csv(ss, filename, row.names = F)


# response time analysis
times <- ts_learning %>% group_by(participant_id) %>% summarise(response_time_nQuick= sum(response_time_lessThan300ms), 
                                                                response_time_median = median(response_time)) %>% arrange(desc(response_time_nQuick))
times
hist(times$response_time_nQuick,breaks = c(0:35))
boxplot(times$response_time_median)
plot(times$response_time_nQuick)
ts_learning %>% group_by(participant_id) %>% count() %>% nrow #count participants
ss %>% filter(!participant_id %in% c(19, 74, 91, 93, 49)) %>% group_by(study_task, study_fsm) %>% count()


# Exclude participants ####
n <- ss %>% filter(!participant_id %in% c(19, 74, 91, 93, 49)) %>%  nrow

filename <- paste0("outputs/", format(Sys.Date(),"%Y-%m-%d"), "_learning_clean", "_an-exp1_n-",n, ".csv")
write.csv(ts_learning %>% filter(!participant_id %in% c(19, 74, 91, 93, 49)), filename, row.names = F)

filename <- paste0("outputs/", format(Sys.Date(),"%Y-%m-%d"), "_transitions_clean", "_an-exp1_n-",n, ".csv")
write.csv(transitions %>% filter(!participant_id %in% c(19, 74, 91, 93, 49)), filename, row.names = F)

filename <- paste0("outputs/", format(Sys.Date(),"%Y-%m-%d"), "_test_prediction_clean", "_an-exp1_n-",n, ".csv")
write.csv(ts_prediction %>% filter(!participant_id %in% c(19, 74, 91, 93, 49)),filename, row.names = F)

filename <- paste0("outputs/", format(Sys.Date(),"%Y-%m-%d"), "_test_control_clean", "_an-exp1_n-",n, ".csv")
write.csv(ts_control %>% filter(!participant_id %in% c(19, 74, 91, 93, 49)), filename, row.names = F)

filename <- paste0("outputs/", format(Sys.Date(),"%Y-%m-%d"), "_test_explanation_clean", "_an-exp1_n-",n, ".csv")
write.csv(ts_explanation %>% filter(!participant_id %in% c(19, 74, 91, 93, 49)), filename, row.names = F)

filename <- paste0("outputs/", format(Sys.Date(),"%Y-%m-%d"), "_participants_clean", "_an-exp1_n-",n, ".csv")
write.csv(ss %>% filter(!participant_id %in% c(19, 74, 91, 93, 49)), filename, row.names = F)

