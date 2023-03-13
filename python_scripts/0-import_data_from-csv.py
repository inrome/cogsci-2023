import pandas as pd
import pickle

# load data from csv files
participants = pd.read_csv('../data_clean/2023-01-28_participants_clean_an-exp1_n-91.csv', sep=",")
trials_learning = pd.read_csv('../data_clean/2023-01-28_learning_clean_an-exp1_n-91.csv', sep=",")
trials_prediction = pd.read_csv('../data_clean/2023-01-28_test_prediction_clean_an-exp1_n-91.csv', sep=",")
trials_control = pd.read_csv('../data_clean/2023-01-28_test_control_clean_an-exp1_n-91.csv', sep=",")
trials_explanation = pd.read_csv('../data_clean/2023-01-28_test_explanation_clean_an-exp1_n-91.csv', sep=",")

# save data as pickle files
with open('../data_clean/imported_clean_data.pickle', 'wb') as f:
    pickle.dump([participants, trials_learning, trials_prediction, trials_control, trials_explanation], f)


#%%

#%%
