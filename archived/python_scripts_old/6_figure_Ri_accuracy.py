import pickle
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#%%

# load data from csv
results = pd.read_csv('../outputs/all_trials_with_Ri.csv', sep=",")

#%%
# based on R_i_mm_esp_0.1, create a new column with 5 bins (0-0.5, 0.51-1, 1.01-1.5, 1.51-2, 2.01-2.5)
bins = pd.IntervalIndex.from_tuples([(0, 0.4), (0.4, 0.8), (0.8, 1.2), (1.2, 1.4), (1.4, 1.6, ), (1.6, 1.8), (1.8, 2.2), (2.2, 2.6)])
results['R_i_bin'] = pd.cut(results['R_i_mm_eps_0.1'], bins=bins)
results['R_i_bin_an'] = pd.cut(results['R_i_mm_an_eps_0.1'], bins=bins)

# create a subset with only the relevant columns for the analysis (participant_id, fsm_type, trial_type, task,
# R_i_bin, R_i_bin_an, response_correct_mm, response_correct_mm_an)

results_accuracy = results[['participant_id', 'fsm_type', 'trial_type', 'task',
                            'R_i_bin', 'R_i_bin_an', 'response_correct_mm', 'response_correct_mm_an']]

#%%
# create R_i_bin_numeric base on the second element in the tuple (e.g. 1 for (0.51, 1))
results_accuracy.loc[:, 'R_i_bin_numeric'] = results_accuracy.loc[:, 'R_i_bin'].apply(lambda x: x.right)

#%%
# show means and 95% confidence intervals for response_correct_mm (y) for each R_i_bin_numeric (x)
sns.set(style="whitegrid", rc = {'figure.figsize':(4.5, 4.5)})

ax = sns.pointplot(data=results_accuracy, x="R_i_bin_numeric", y="response_correct_mm", hue="fsm_type",
                   errorbar=('ci', 95), dodge=True)
plt.axhline(y=0.5, color='r', linestyle='--') # add line at 0.5
plt.show()
#%%