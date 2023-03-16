import pickle
import pandas as pd
import numpy as np
import math


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
    log_p_answers = {'visible': [], 'hidden': [], 'hidden_an': []}

    for index, row in trials_vis.iterrows():
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

    for index, row in trials_hid.iterrows():
        if task == 'explanation':
            option_1 = 1
            option_2 = 2
        else:
            option_1 = row['option_1']
            option_2 = row['option_2']
        log_p_answer = compute_log_p_answer(task, row['response'],
                                            option_1, option_2,
                                            row['option_1_p_mm'],
                                            row['option_2_p_mm'],
                                            row['R_i_mm_eps_0.1'], beta)
        log_p_answers["hidden"].append(log_p_answer)

        log_p_answer = compute_log_p_answer(task, row['response'],
                                            option_1, option_2,
                                            row['option_1_p_mm_an'],
                                            row['option_2_p_mm_an'],
                                            row['R_i_mm_an_eps_0.1'],
                                            beta)
        log_p_answers["hidden_an"].append(log_p_answer)

    return log_p_answers


# %%
with open('../outputs/trials_with_Ri.pickle', 'rb') as f:
    sample = pickle.load(f)

with open('../data_clean/imported_clean_data.pickle', 'rb') as f:
    imported_data = pickle.load(f)

imported_participants = imported_data[0]
# %%

beta_range = np.arange(0, 1.1, 0.1)  # set range of beta values
#participant_id = 69  # set participant id
for participant_id in sample.keys():
    trials_vis = sample[participant_id]['trials_vis']
    trials_hid = sample[participant_id]['trials_hid']
    task = sample[participant_id]['task']

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

    # create dataframe with sum_log_p_answers for each beta value
    df = pd.DataFrame.from_dict(sum_log_p_answers, orient='index')

    # find beta value with the highest sum_log_p_answer
    max_beta = df.idxmax(axis=0)

    # calculate predicted probabilities for max_beta
    predicted_accuracy = {}
    for row_index, row in max_beta.iteritems():
        condition = row_index
        max_beta_condition = row
        R_i = 2
        predicted_accuracy[condition] = (math.e ** (R_i * max_beta_condition)) / (
                    math.e ** (R_i * max_beta_condition) + math.e ** (-1 * R_i * max_beta_condition))

    # if trials_vis['response_correct_mm'] has more than 2 non-NaN values, calculate mean
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

#%%
# save sample to pickle file
with open('../outputs/trials_with_max_beta.pickle', 'wb') as f:
    pickle.dump(sample, f)
#%%

# export 'predicted_accuracy' to csv file:
results_all = pd.DataFrame()
for participant_id in sample.keys():
    results = pd.DataFrame()
    results = results.append(sample[participant_id]['predicted_accuracy'], ignore_index=True)
    # add participant_id to results
    results['participant_id'] = participant_id
    # add task to results
    results['task'] = sample[participant_id]['task']

    # relocate participant_id and task to first and second column
    results = results[['participant_id', 'task', 'visible', 'hidden', 'hidden_an']]


    # reformat results condition columns (visible, hidden, hidden_an) into long format
    results = pd.melt(results, id_vars=['participant_id', 'task'], value_vars=['visible', 'hidden', 'hidden_an'],
                      var_name='condition', value_name='predicted_accuracy')

    # add fsm to results
    results['fsm'] = imported_participants[imported_participants['participant_id'] == participant_id]['study_fsm'].values[0]

    #add mm_accuracy to results
    results_accuracy = pd.DataFrame()
    results_accuracy = results_accuracy.append(sample[participant_id]['mm_accuracy'], ignore_index=True)

    #add column 'mm_accuracy' to results and fill with values from results_accuracy
    for index, row in results.iterrows():
        results.loc[index, 'mm_accuracy'] = results_accuracy.loc[0, row['condition']]

    #add column 'count_nan' to results and fill with values from results_accuracy
    results_count_nan = pd.DataFrame()
    results_count_nan = results_count_nan.append(sample[participant_id]['count_nan'], ignore_index=True)
    for index, row in results.iterrows():
        results.loc[index, 'count_nan'] = results_count_nan.loc[0, row['condition']]

    results_all = results_all.append(results, ignore_index=True)

results_all.to_csv('../outputs/predicted_accuracy.csv', index=False)