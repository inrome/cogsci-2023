import pickle
import numpy as np
import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
data_with_PEC_and_Ri_path = os.path.join(current_dir, '../outputs/trials_with_Ri.pickle')

with open(data_with_PEC_and_Ri_path, 'rb') as f:
    sample = pickle.load(f)

#%%
for participant_id in sample.keys():
    trials_vis = sample[participant_id]['trials_vis']
    trials_hid = sample[participant_id]['trials_hid']
    task = sample[participant_id]['task']

    for index, row in trials_vis.iterrows():
        option_1_p = row['option_1_p_mm']
        option_2_p = row['option_2_p_mm']

        response = row['response']

        if option_1_p != option_2_p:
            if task == 'explanation':
                option_1 = 1
                option_2 = 2
                correct_mm = option_1 if option_1_p < option_2_p else option_2
            elif task == 'prediction':
                option_1 = row['option_1']
                option_2 = row['option_2']
                correct_mm = option_1 if option_1_p > option_2_p else option_2
            elif task == 'control':
                option_1 = "a"
                option_2 = "b"
                correct_mm = option_1 if option_1_p > option_2_p else option_2
            else:
                correct_mm = None

        if correct_mm is None:
            response_correct_mm = np.nan
        else:
            response_correct_mm = 1 if response == correct_mm else 0

        trials_vis.loc[index, 'response_correct_mm'] = response_correct_mm

    for index, row in trials_hid.iterrows():
        option_1_p = row['option_1_p_mm']
        option_2_p = row['option_2_p_mm']
        response = row['response']

        if option_1_p != option_2_p:
            if task == 'explanation':
                option_1 = 1
                option_2 = 2
                correct_mm = option_1 if option_1_p < option_2_p else option_2
            else:
                option_1 = row['option_1']
                option_2 = row['option_2']
                correct_mm = option_1 if option_1_p > option_2_p else option_2
        else:
            correct_mm = None

        if correct_mm is None:
            response_correct_mm = np.nan
        else:
            response_correct_mm = 1 if response == correct_mm else 0

        trials_hid.loc[index, 'response_correct_mm'] = response_correct_mm

        # the same for the an model
        option_1_p = row['option_1_p_mm_an']
        option_2_p = row['option_2_p_mm_an']

        if option_1_p != option_2_p:
            if task == 'explanation':
                option_1 = 1
                option_2 = 2
                correct_mm = option_1 if option_1_p < option_2_p else option_2
            else:
                option_1 = row['option_1']
                option_2 = row['option_2']
                correct_mm = option_1 if option_1_p > option_2_p else option_2
        else:
            correct_mm = None

        if correct_mm is None:
            response_correct_mm_an = np.nan
        else:
            response_correct_mm_an = 1 if response == correct_mm else 0

        trials_hid.loc[index, 'response_correct_mm_an'] = response_correct_mm_an

    sample[participant_id]['trials_vis'] = trials_vis
    sample[participant_id]['trials_hid'] = trials_hid

# save data as an updated pickle file

with open(data_with_PEC_and_Ri_path, 'wb') as f:
    pickle.dump(sample, f)

#
# %%
