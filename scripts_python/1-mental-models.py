import pandas as pd
import numpy as np
import os
import pickle

# Load data from pickle file
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, '../data/')

# load data from csv files
participants = pd.read_csv(data_path + 'participants.csv')
trials_learning = pd.read_csv(data_path + 'trials_learning.csv')
trials_prediction = pd.read_csv(data_path + 'trials_prediction.csv')
trials_control = pd.read_csv(data_path + 'trials_control.csv')
trials_explanation = pd.read_csv(data_path + 'trials_explanation.csv')

# %%
mental_models = {}
states = [0, 1, 2, 3]
responses = ['a', 'b']

for participant_id in trials_learning.participant_id.unique():

    df_learning = trials_learning[trials_learning['participant_id'] == participant_id]

    fsm = {}  # set up priors
    alpha = 0.001 # pseudocount

    for state in states:
        fsm[state] = {}
        for response in responses:
            fsm[state][response] = np.array([alpha] * 4) # sets prior probabilities

    for index, row in df_learning.iterrows():
        state_current = int(row['state_current'])
        response_current = row['response_current']
        state_next = int(row['state_next'])
        fsm[state_current][response_current][state_next] += 1 # adds 1 to the observed transition


    for state in states:
        for response in responses:
            tot = fsm[state][response].sum() # total number of observed transitions
            fsm[state][response] = np.array([x/tot for x in fsm[state][response]])  # normalizes the values

            assert round(fsm[state][response].sum(), 2) == 1, "Error: probabilities don't sum to 1"

    mental_models[participant_id] = fsm
#%%

# save mental models to pickle file
save_path = os.path.join(current_dir, '../outputs/mental_models.pickle')

with open(save_path, 'wb') as f:
    pickle.dump(mental_models, f)
