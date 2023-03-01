import pickle
import numpy as np
import pandas as pd
import itertools

# Load data from pickle file
with open('../data_clean/imported_clean_data.pickle', 'rb') as f:
    participants, transitions, trials_learning, trials_prediction, trials_control, trials_explanation = pickle.load(f)
# %%
mental_models = {}
mental_models_df = pd.DataFrame()
states = [0, 1, 2, 3]
responses = ['a', 'b']

for participant_id in trials_learning.participant_id.unique():
    # create a new dataframe with all possible combinations of state_current ([0, 1, 2, 3]), response_current (['a', 'b']), state_next([0, 1, 2, 3])
    df = pd.DataFrame(list(itertools.product(states, responses, states)),
                      columns=['state_current', 'response_current', 'state_next'])

    # load data for current participant
    df_learning = trials_learning[trials_learning['participant_id'] == participant_id]

    # calculate number of trials for each state_current, response_current, state_next
    counts = df_learning.groupby(['state_current', 'response_current', 'state_next']).size().reset_index(name='counts')

    # merge the two dataframes
    df = pd.merge(df, counts, how='left', on=['state_current', 'response_current', 'state_next'])

    # add transition_id as a first column to dataframe (concatenation of state_current, response_current, state_next)
    df.insert(0, 'transition_id', df['state_current'].astype(str) + df['response_current'] + df['state_next'].astype(str))

    # fill NaN values with 0 (for counts)
    df = df.fillna(0)

    # calculate state_next_p as counts / total counts for each state_current, response_current
    df['state_next_p'] = df.groupby(['state_current', 'response_current'])['counts'].apply(lambda x: x / x.sum())

    # if state_next_p is NaN, set it to 0.25 (uniform distribution)
    df['state_next_p'] = df['state_next_p'].fillna(0.25)

    # reformat mental model as dictionary
    MM = {}
    for state_current in states:
        inputs = {}
        for inp in responses:
            inputs[inp] = np.array([df.state_next_p[
                                        (df.state_current == state_current) & (df.response_current == inp) & (
                                                    df.state_next == 0)].item(),
                                    df.state_next_p[
                                        (df.state_current == state_current) & (df.response_current == inp) & (
                                                    df.state_next == 1)].item(),
                                    df.state_next_p[
                                        (df.state_current == state_current) & (df.response_current == inp) & (
                                                    df.state_next == 2)].item(),
                                    df.state_next_p[
                                        (df.state_current == state_current) & (df.response_current == inp) & (
                                                    df.state_next == 3)].item()])
        MM[state_current] = {"a": inputs["a"], "b": inputs["b"]}

    # add mental model to dictionary
    mental_models[participant_id] = MM

    # add df to dataframe with all mental models
    mental_models_df = mental_models_df.append(df)

# save mental models to pickle file
with open('../outputs/mental_models.pickle', 'wb') as f:
    pickle.dump(mental_models, f)

# save mental models to csv file
mental_models_df.to_csv('../outputs/mental_models_updated.csv', index=False)
#%%
