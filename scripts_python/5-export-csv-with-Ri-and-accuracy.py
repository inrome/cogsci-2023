import pickle
import pandas as pd
import os 

current_dir = os.path.dirname(os.path.abspath(__file__))
data_with_PEC_and_Ri_path = os.path.join(current_dir, '../outputs/trials_with_Ri.pickle')

with open(data_with_PEC_and_Ri_path, 'rb') as f:
    sample = pickle.load(f)
    
#%%
results = pd.DataFrame()
for participant_id in sample.keys():
    trials = pd.concat([sample[participant_id]['trials_vis'],
                        sample[participant_id]['trials_hid']])
    trials = trials.sort_values(by=['trial_number'])
    results = pd.concat([results, trials], ignore_index=True)

#%%

results.to_csv(os.path.join(current_dir, '../outputs/all_trials_with_Ri.csv') , sep=',', index=False)