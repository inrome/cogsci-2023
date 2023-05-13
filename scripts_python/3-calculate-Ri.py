import pickle
import pandas as pd
import numpy as np
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
data_with_PEC_path = os.path.join(current_dir, '../outputs/trials_with_PEC_mm.pickle')

with open(data_with_PEC_path, 'rb') as f:
    sample = pickle.load(f)


def compute_Ri(option_1_p, option_2_p, epsilon):
    import math
    # abs value of log ratio of probabilities
    r_i = abs(math.log((option_1_p + epsilon) / (option_2_p + epsilon)))

    return r_i


epsilon = 0.1  # set value for epsilon

for participant_id in sample.keys():
    trials_vis = sample[participant_id]['trials_vis']
    trials_hid = sample[participant_id]['trials_hid']
    task = sample[participant_id]['task']

    for index, row in trials_vis.iterrows():
        trials_vis.loc[index, 'R_i_mm_eps_' + str(epsilon)] = compute_Ri(row['option_1_p_mm'], row['option_2_p_mm'],
                                                                         epsilon)
    for index, row in trials_hid.iterrows():
        trials_hid.loc[index, 'R_i_mm_eps_' + str(epsilon)] = compute_Ri(row['option_1_p_mm'], row['option_2_p_mm'],
                                                                         epsilon)

        trials_hid.loc[index, 'R_i_mm_an_eps_' + str(epsilon)] = compute_Ri(row['option_1_p_mm_an'],
                                                                            row['option_2_p_mm_an'], epsilon)

    # save data
    sample[participant_id]['trials_vis'] = trials_vis
    sample[participant_id]['trials_hid'] = trials_hid
    
    save_path = os.path.join(current_dir, '../outputs/trials_with_Ri.pickle')

    with open(save_path, 'wb') as f:
        pickle.dump(sample, f)
#%%
