import pickle
import pandas as pd
import numpy as np
import math
import os 
import matplotlib.pyplot as plt
import seaborn as sns

# %%
def compute_log_p_answer(task, response,
                         option_1, option_2,
                         option_1_p, option_2_p, r_i, beta):
    import math

    p_correct = (math.e ** (r_i * beta)) / (math.e ** (r_i * beta) + math.e ** (-1 * r_i * beta))

    if task == "explanation":
        correct_mm = option_1 if option_1_p < option_2_p else option_2
    else:
        correct_mm = option_1 if option_1_p > option_2_p else option_2

    p_answer = p_correct if response == correct_mm else (1 - p_correct)

    log_p_answer = math.log(p_answer)

    return log_p_answer

# %%
def compute_log_p_answer_for_trials(trials_vis, trials_hid, task, beta):
    log_p_answers = {'visible': [], 'hidden': [], 'hidden_an': [], 
                     'hidden_normative_subset': [], 'hidden_an_subset': []}

    # visible trials
    for index, row in trials_vis.iterrows():
        # fix option values
        if task == 'explanation':
            option_1 = 1
            option_2 = 2
        elif task == 'prediction':
            option_1 = row['option_1']
            option_2 = row['option_2']
        elif task == 'control':
            option_1 = "a"
            option_2 = "b"
        else:
            raise ValueError("task must be 'explanation', 'prediction' or 'control'")

        log_p_answer = compute_log_p_answer(task, row['response'],
                                            option_1, option_2,
                                            row['option_1_p_mm'],
                                            row['option_2_p_mm'],
                                            row['R_i_mm_eps_0.1'], beta)
        log_p_answers["visible"].append(log_p_answer)

    # hidden trials
    for index, row in trials_hid.iterrows():
        if task == 'explanation':
            option_1 = 1
            option_2 = 2
        else:
            option_1 = row['option_1']
            option_2 = row['option_2']
        
        # Normative model
        log_p_answer = compute_log_p_answer(task, row['response'],
                                            option_1, option_2,
                                            row['option_1_p_mm'],
                                            row['option_2_p_mm'],
                                            row['R_i_mm_eps_0.1'], beta)
        
        log_p_answers["hidden"].append(log_p_answer)
        
        # Normative model: Only consider AN-sensitive trials
        if abs(row['R_i_mm_eps_0.1'] - row['R_i_mm_an_eps_0.1']) > 0.1 or \
            row['response_correct_mm'] != row['response_correct_mm_an']:

            log_p_answers["hidden_normative_subset"].append(log_p_answer)

        # Alternative neglect model
        log_p_answer = compute_log_p_answer(task, row['response'],
                                            option_1, option_2,
                                            row['option_1_p_mm_an'],
                                            row['option_2_p_mm_an'],
                                            row['R_i_mm_an_eps_0.1'],
                                            beta)
        
        log_p_answers["hidden_an"].append(log_p_answer)
        # Alternative neglect model: Only consider AN-sensitive trials
        if abs(row['R_i_mm_eps_0.1'] - row['R_i_mm_an_eps_0.1']) > 0.1 or \
            row['response_correct_mm'] != row['response_correct_mm_an']:
            log_p_answers["hidden_an_subset"].append(log_p_answer)

    return log_p_answers


# %%
current_dir = os.path.dirname(os.path.abspath(__file__))
data_with_Ri_path = os.path.join(current_dir, '../outputs/trials_with_Ri.pickle')
data_imported_path = os.path.join(current_dir, '../data/imported_clean_data.pickle')

with open(data_with_Ri_path, 'rb') as f:
    sample = pickle.load(f)

with open(data_imported_path, 'rb') as f:
    imported_data = pickle.load(f)

imported_participants = imported_data[0]
# %%

beta_range = np.arange(0, 1.1, 0.005)  # set range of beta values
#participant_id = 69  # set participant id
big_sum_log_p_answers = {}
for task in ['explanation', 'prediction', 'control']:
    big_sum_log_p_answers[task] = {}
    for fsm_type in ['easy', 'hard']:
        big_sum_log_p_answers[task][fsm_type] = {}
        for condition in ['visible', 'hidden', 'hidden_an', 'hidden_normative_subset', 'hidden_an_subset']:
            big_sum_log_p_answers[task][fsm_type][condition] = {}
            for beta in beta_range:
                big_sum_log_p_answers[task][fsm_type][condition][beta]=0

for participant_id in sample.keys():
    trials_vis = sample[participant_id]['trials_vis']
    trials_hid = sample[participant_id]['trials_hid']
    task = sample[participant_id]['task']
    fsm_type = sample[participant_id]['trials_vis']['fsm_type'].iloc[0]

    # compute log p answer for each beta value
    all_betas = {}
    for beta in beta_range:
        all_betas[beta] = compute_log_p_answer_for_trials(trials_vis, trials_hid, task, beta)

    # sum log p answers for each beta value
    sum_log_p_answers = {}
    for beta in beta_range:
        sum_log_p_answers[beta] = {}
        for condition in all_betas[beta].keys():
            sum_log_p_answers[beta][condition] = sum(all_betas[beta][condition])
            big_sum_log_p_answers[task][fsm_type][condition][beta] += sum(all_betas[beta][condition])

    # create dataframe with sum_log_p_answers for each beta value
    df = pd.DataFrame.from_dict(sum_log_p_answers, orient='index')

    # find beta value with the highest sum_log_p_answer
    max_beta = df.idxmax(axis=0)

    # calculate predicted probabilities for max_beta
    predicted_accuracy = {}
    for row_index, row in max_beta.items():
        condition = row_index
        max_beta_condition = row
        R_i = 2
        predicted_accuracy[condition] = (math.e ** (R_i * max_beta_condition)) / (
                    math.e ** (R_i * max_beta_condition) + math.e ** (-1 * R_i * max_beta_condition))

    # if trials_vis['response_correct_mm'] has more than 5 NaNs, set accuracy to NaN
    mm_accuracy = {}
    mm_accuracy['visible'] = trials_vis['response_correct_mm'].mean(skipna = True) if \
        trials_vis['response_correct_mm'].isna().sum() < 5 else np.nan
    mm_accuracy['hidden'] = trials_hid['response_correct_mm'].mean(skipna = True) if \
        trials_hid['response_correct_mm'].isna().sum() < 5 else np.nan
    mm_accuracy['hidden_an'] = trials_hid['response_correct_mm_an'].mean(skipna = True) if \
        trials_hid['response_correct_mm_an'].isna().sum() < 5 else np.nan

    count_nan = {}
    count_nan['visible'] = trials_vis['response_correct_mm'].isna().sum()
    count_nan['hidden'] = trials_hid['response_correct_mm'].isna().sum()
    count_nan['hidden_an'] = trials_hid['response_correct_mm_an'].isna().sum()

    # add max_beta and predicted_accuracy to sample
    sample[participant_id]['max_beta'] = max_beta
    sample[participant_id]['predicted_accuracy'] = predicted_accuracy
    sample[participant_id]['mm_accuracy'] = mm_accuracy
    sample[participant_id]['count_nan'] = count_nan
    sample[participant_id]['hidden_subset_count'] = len(all_betas[0.0]['hidden_an_subset'])
#%%

# subset prediction easy visible trials from big_sum_log_p_answers
big_sum_log_p_answers_subset = big_sum_log_p_answers['prediction']['easy']['visible']

# find max beta for each task, fsm_type and condition
max_beta = {}
max_beta_df = pd.DataFrame()

for task in ['explanation', 'prediction', 'control']:
    max_beta[task] = {}
    for fsm_type in ['easy', 'hard']:
        max_beta[task][fsm_type] = {}
        for condition in ['visible', 'hidden', 'hidden_an', 'hidden_normative_subset', 'hidden_an_subset']:
            max_beta[task][fsm_type][condition] = {}
            tmp_betas = pd.DataFrame.from_dict(big_sum_log_p_answers[task][fsm_type][condition], orient='index')
            max_beta[task][fsm_type][condition] = tmp_betas.idxmax(axis=0)
            max_log_p = tmp_betas.max(axis=0)
            this_max_beta = max_beta[task][fsm_type][condition].iloc[0]

            # select values with indext 0.1 or lower form tmp_betas
            tmp_bet_low = tmp_betas.loc[tmp_betas.index < this_max_beta].iloc[:,0]
            tmp_bet_high = tmp_betas.loc[tmp_betas.index > this_max_beta].iloc[:,0]
            
            # find index of value that is lower that max_log_p by 1
            tmp_bet_low = tmp_bet_low.loc[tmp_bet_low < max_log_p.iloc[0] - 2].idxmax(axis=0) if \
                tmp_bet_low.loc[tmp_bet_low < max_log_p.iloc[0] - 2].shape[0] > 0 else 0
            tmp_bet_high = tmp_bet_high.loc[tmp_bet_high < max_log_p.iloc[0] - 2].idxmax(axis=0) if \
                tmp_bet_high.loc[tmp_bet_high < max_log_p.iloc[0] - 2].shape[0] > 0 else 0

            # create temporary dataframe to store values for this task, fsm_type and condition
            tmp_df = pd.DataFrame()
            tmp_df['beta_max'] = max_beta[task][fsm_type][condition]
            tmp_df['beta_lower'] = tmp_bet_low
            tmp_df['beta_higher'] = tmp_bet_high
            tmp_df['task'] = task
            tmp_df['fsm_type'] = fsm_type
            tmp_df['condition'] = condition

            max_beta_df = pd.concat([max_beta_df, tmp_df], axis=0)


df = max_beta_df.loc[(max_beta_df['condition'].isin(['visible', 'hidden', 'hidden_an']))]

# export df to csv
df.to_csv(os.path.join(current_dir, '../outputs/beta_with_plus_minus_2LL_errors.csv'))

# save sample to pickle file
save_path = os.path.join(current_dir, '../outputs/trials_with_max_beta.pickle')
with open(save_path, 'wb') as f:
    pickle.dump(sample, f)


# %%
