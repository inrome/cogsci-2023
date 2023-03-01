library(tidyverse)

df <- read.csv("outputs/2023-03-01_all_trials_with_Ri_v2.csv")

# add bins 
df <-  df %>% mutate(R_i_bin = cut(R_i_mm_eps_0.1, breaks = c(0, 0.5, 1, 1.5, 2, 2.5))) %>% filter(!is.na(R_i_bin)) %>% 
  mutate(task = fct_recode(task,  "Prediction" = "prediction", "Control" = 'control', "Explanation" = "explanation"),
         task = fct_relevel(task,  c("Prediction","Control","Explanation")))

ggplot(df, aes(R_i_bin, response_correct_mm, color = trial_type)) + 
  stat_summary(fun.data = mean_cl_boot, position = position_dodge(0.4)) + 
  geom_hline(yintercept = 0.5) + facet_grid(fsm_type ~ task)
