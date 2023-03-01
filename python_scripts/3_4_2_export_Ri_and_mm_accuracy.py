import pickle
import pandas as pd

with open('../outputs/trials_with_Ri.pickle', 'rb') as f:
    sample = pickle.load(f)
    
#%%
results = pd.DataFrame()
for participant_id in sample.keys():
    trials = pd.concat([sample[participant_id]['trials_vis'],
                        sample[participant_id]['trials_hid']])
    trials = trials.sort_values(by=['trial_number'])
    trials['task'] = sample[participant_id]['task']
    results = pd.concat([results, trials])

#%%
results.to_csv('../outputs/2023-03-01_all_trials_with_Ri_v2.csv', sep=',', index=False)