#%%
import numpy as np
import pandas as pd
import pickle
import os
from PEC_functions import predict, control, explain

# %%
# get trials from imported data
def get_trials_and_tasks(trials_prediction, trials_control, trials_explanation, participant_id):
    trials_vis, trials_hid, task = None, None, None

    if trials_prediction[trials_prediction.participant_id == participant_id].size > 0:
        trials_vis = trials_prediction[(trials_prediction.participant_id == participant_id) &
                                       (trials_prediction.trial_type == "visible")]
        trials_hid = trials_prediction[(trials_prediction.participant_id == participant_id) &
                                       (trials_prediction.trial_type == "hidden")]
        task = "prediction"

    if trials_control[trials_control.participant_id == participant_id].size > 0:
        trials_vis = trials_control[(trials_control.participant_id == participant_id) &
                                    (trials_control.trial_type == "visible")]
        trials_hid = trials_control[(trials_control.participant_id == participant_id) &
                                    (trials_control.trial_type == "hidden")]
        task = "control"

    if trials_explanation[trials_explanation.participant_id == participant_id].size > 0:
        trials_vis = trials_explanation[(trials_explanation.participant_id == participant_id) &
                                        (trials_explanation.trial_type == "visible")]
        trials_hid = trials_explanation[(trials_explanation.participant_id == participant_id) &
                                        (trials_explanation.trial_type == "hidden")]
        task = "explanation"

    return trials_vis, trials_hid, task


def calculate_probabilities(trials_vis_in, trials_hid_in, MM, task):
    import numpy as np
    trials_vis=trials_vis_in.copy()
    trials_hid=trials_hid_in.copy()
    #  add columns for probabilities
    trials_vis["option_1_p_mm"] = np.nan
    trials_vis["option_2_p_mm"] = np.nan
    trials_hid["option_1_p_mm"] = np.nan
    trials_hid["option_2_p_mm"] = np.nan
    trials_hid["option_1_p_mm_an"] = np.nan
    trials_hid["option_2_p_mm_an"] = np.nan

    if task == "prediction":
        # Visible
        for index, row in trials_vis.iterrows():
            state_2 = int(row['state_2'])
            response_2 = row['response_2']
            option_1 = int(row['option_1'])
            option_2 = int(row['option_2'])
            trials_vis.loc[index, 'option_1_p_mm'] = MM[state_2][response_2][option_1]
            trials_vis.loc[index, 'option_2_p_mm'] = MM[state_2][response_2][option_2]

        # Hidden
        for index, row in trials_hid.iterrows():
            state_1 = int(row['state_1'])
            response_1 = row['response_1']
            response_2 = row['response_2']
            option_1 = int(row['option_1'])
            option_2 = int(row['option_2'])

            trials_hid.loc[index, 'option_1_p_mm'] = predict(state_1, response_1, response_2, MM,
                                                             mode="normative")[option_1][0]
            trials_hid.loc[index, 'option_2_p_mm'] = predict(state_1, response_1, response_2, MM,
                                                             mode="normative")[option_2][0]

            trials_hid.loc[index, 'option_1_p_mm_an'] = predict(state_1, response_1, response_2, MM,
                                                                mode="an")[option_1][0]
            trials_hid.loc[index, 'option_2_p_mm_an'] = predict(state_1, response_1, response_2, MM,
                                                                mode="an")[option_2][0]

    elif task == "control":
        # Visible
        for index, row in trials_vis.iterrows():
            state_2 = int(row['state_2'])
            state_3 = int(row['state_3'])
            option_1 = "a"
            option_2 = "b"
            trials_vis.loc[index, 'option_1_p_mm'] = MM[state_2][option_1][state_3]
            trials_vis.loc[index, 'option_2_p_mm'] = MM[state_2][option_2][state_3]

        # Hidden
        for index, row in trials_hid.iterrows():
            state_1 = int(row['state_1'])
            state_3 = int(row['state_3'])
            option_1 = row['option_1']
            option_2 = row['option_2']

            trials_hid.loc[index, 'option_1_p_mm'] = control(state_1, state_3, MM,
                                                             mode="normative")[option_1]
            trials_hid.loc[index, 'option_2_p_mm'] = control(state_1, state_3, MM,
                                                             mode="normative")[option_2]

            trials_hid.loc[index, 'option_1_p_mm_an'] = control(state_1, state_3, MM,
                                                                mode="an")[option_1]
            trials_hid.loc[index, 'option_2_p_mm_an'] = control(state_1, state_3, MM,
                                                                mode="an")[option_2]
    elif task == "explanation":
        # Visible
        for index, row in trials_vis.iterrows():
            state_1 = int(row['state_1'])
            response_1 = row['response_1']
            state_2 = int(row['state_2'])
            response_2 = row['response_2']
            state_3 = int(row['state_3'])

            response_1_cf = "a" if response_1 == "b" else "b"
            response_2_cf = "a" if response_2 == "b" else "b"
            trials_vis.loc[index, 'option_1_p_mm'] = MM[state_1][response_1_cf][state_2] * \
                                                     MM[state_2][response_2][state_3]
            trials_vis.loc[index, 'option_2_p_mm'] = MM[state_1][response_1][state_2] * \
                                                     MM[state_2][response_2_cf][state_3]

        # Hidden
        for index, row in trials_hid.iterrows():
            state_1 = int(row['state_1'])
            response_1 = row['response_1']
            response_2 = row['response_2']
            state_3 = int(row['state_3'])
            trials_hid.loc[index, 'option_1_p_mm'] = explain(state_1, response_1, response_2, state_3, MM,
                                                             mode="normative")["1"]
            trials_hid.loc[index, 'option_2_p_mm'] = explain(state_1, response_1, response_2, state_3, MM,
                                                             mode="normative")["2"]

            trials_hid.loc[index, 'option_1_p_mm_an'] = explain(state_1, response_1, response_2,
                                                                state_3, MM, mode="an")["1"]
            trials_hid.loc[index, 'option_2_p_mm_an'] = explain(state_1, response_1, response_2,
                                                                state_3, MM, mode="an")["2"]

    return trials_vis, trials_hid
# %%

# load data
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, '../data/imported_clean_data.pickle')

with open(data_path, 'rb') as f:
    participants, trials_learning, trials_prediction, trials_control, trials_explanation = pickle.load(f)

mm_path = os.path.join(current_dir, '../outputs/mental_models.pickle')

with open(mm_path, 'rb') as f:
    MM = pickle.load(f)

# %%

trials_with_PEC_mm = {}
for participant_id in participants.participant_id.unique():
    # get trials and task
    trials_vis, trials_hid, task = get_trials_and_tasks(trials_prediction, trials_control, trials_explanation,
                                                        participant_id)

    # get mental model
    mm = MM[participant_id]

    # calculate probabilities
    trials_vis_new, trials_hid_new = calculate_probabilities(trials_vis, trials_hid, mm, task)

    # save
    trials_with_PEC_mm[participant_id] = {"trials_vis": trials_vis_new,
                                          "trials_hid": trials_hid_new,
                                          "task": task,
                                          "MM": mm}
    
    save_path = os.path.join(current_dir, '../outputs/trials_with_PEC_mm.pickle')
    
    with open(save_path, "wb") as f:
        pickle.dump(trials_with_PEC_mm, f)
# %%
