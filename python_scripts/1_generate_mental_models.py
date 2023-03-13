import pickle
import numpy as np
import pandas as pd
import itertools

# Load data from pickle file
with open('../data_clean/imported_clean_data.pickle', 'rb') as f:
    participants, trials_learning, trials_prediction, trials_control, trials_explanation = pickle.load(f)
# %%
mental_models = {}
states = [0, 1, 2, 3]
responses = ['a', 'b']

for participant_id in trials_learning.participant_id.unique():

    df_learning = trials_learning[trials_learning['participant_id'] == participant_id]

    fsm = {}  # set up empty dictionary to store mental model

    for state in states:
        fsm[state] = {}
        fsm[state]["a"] = np.array([1/4.0, 1/4.0, 1/4.0, 1/4.0])
        fsm[state]["b"] = np.array([1/4.0, 1/4.0, 1/4.0, 1/4.0])

    for index, row in df_learning.iterrows():
        state_current = int(row['state_current'])
        response_current = row['response_current']
        state_next = int(row['state_next'])
        fsm[state_current][response_current][state_next] += 1

    for state in states:
        tot_a = fsm[state]["a"].sum() * 1.0
        fsm[state]["a"] = [x/tot_a for x in fsm[state]["a"]]
        tot_b = fsm[state]["b"].sum() * 1.0
        fsm[state]["b"] = [x/tot_b for x in fsm[state]["b"]]

    mental_models[participant_id] = fsm
#%%

# save mental models to pickle file
with open('../outputs/mental_models.pickle', 'wb') as f:
    pickle.dump(mental_models, f)

#%%
