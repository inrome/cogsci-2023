import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# load data from csv file
results = pd.read_csv('../../outputs/2023-01-28_all_trials_with_Ri_v2.csv', sep=",")

# select only the relevant columns for the analysis: participant_id, fsm_type, trial_type, task,
# R_i_mm_eps_0.1, R_i_mm_am_eps_0.1, response_correct
results = results[['participant_id', 'fsm_type', 'trial_type', 'task',
                   'R_i_mm_eps_0.1', 'R_i_mm_an_eps_0.1', 'response_correct']]
# convert response_correct to integer
results['response_correct'] = results['response_correct'].astype(int)
#%%
# plot histogram of Ri for prediction task for each fsm_type and trial_type
sns.set(style="whitegrid", rc = {'figure.figsize':(4.5, 4.5)})
ax = sns.histplot(data=results[(results['task'] == 'prediction')],
                    x="R_i_mm_eps_0.1", multiple="dodge", bins=10)
g = (sns.FacetGrid(data = results[(results['task'] == 'prediction')],
                     col="fsm_type", row="trial_type", hue="fsm_type", height=4.5, aspect=1.5).
     map(sns.histplot, "R_i_mm_eps_0.1", bins=10).add_legend())
plt.show()
#%%
# the same for "control" task
sns.set(style="whitegrid", rc = {'figure.figsize':(4.5, 4.5)})
ax = sns.histplot(data=results[(results['task'] == 'control')],
                    x="R_i_mm_eps_0.1", multiple="dodge", bins=10)
g = (sns.FacetGrid(data = results[(results['task'] == 'control')],
                        col="fsm_type", row="trial_type", hue="fsm_type", height=4.5, aspect=1.5).
        map(sns.histplot, "R_i_mm_eps_0.1", bins=10).add_legend())
plt.show()

#%%
# the same for "explanation" task
sns.set(style="whitegrid", rc = {'figure.figsize':(4.5, 4.5)})
ax = sns.histplot(data=results[(results['task'] == 'explanation')],
                    x="R_i_mm_eps_0.1", multiple="dodge", bins=10)
g = (sns.FacetGrid(data = results[(results['task'] == 'explanation')],
                        col="fsm_type", row="trial_type", hue="fsm_type", height=4.5, aspect=1.5).
        map(sns.histplot, "R_i_mm_eps_0.1", bins=10).add_legend())
plt.show()

#%%
# add R_i_mm_eps_0.1_bin column to results
results['R_i_mm_eps_0.1_bin'] = pd.cut(results['R_i_mm_eps_0.1'], bins=4)

# calculate mean response_correct for each Ri value for each task, fsm_type and trial_type
grouped_accuracy = results.groupby(['task', 'fsm_type', 'trial_type', 'R_i_mm_eps_0.1_bin']).mean()