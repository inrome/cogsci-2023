import pandas as pd
import pickle
import numpy as np
#%%
# export mental models to csv for participants 22, 78 and 69

# load mental models
with open('../outputs/mental_models.pickle', 'rb') as f:
    mental_models = pickle.load(f)

for participant_id in [22, 78, 69]:
    mm = pd.DataFrame(columns=['state_current', 'response_current', 'state_next', 'state_next_p'])
    for state_current in range(4):
        for response_current in ['a', 'b']:
            for state_next in range(4):
                mm = mm.append({'state_current': state_current,
                                'response_current': response_current,
                                'state_next': state_next,
                                'state_next_p': mental_models[participant_id][state_current][response_current][state_next]},
                               ignore_index=True)
    mm.to_csv('../outputs/mental_model_{}.csv'.format(participant_id), sep=',', index=False)

#%%
# export test trials for participants 22, 78 and 69
# load data from pickle file
with open('../outputs/trials_with_Ri.pickle', 'rb') as f:
    sample = pickle.load(f)

for participant_id in [22, 78, 69]:
    trials = pd.concat([sample[participant_id]['trials_vis'],
                        sample[participant_id]['trials_hid']])
    trials = trials.sort_values(by=['trial_number'])
    trials.to_csv('../outputs/test_trials_{}.csv'.format(participant_id), sep=',', index=False)

#%%
# export max beta for participants 22, 78 and 69
# load data from pickle file
with open('../outputs/trials_with_max_beta.pickle', 'rb') as f:
    sample = pickle.load(f)

print(sample[22]['max_beta'])
print(sample[78]['max_beta'])
print(sample[69]['max_beta'])