# import modules
import numpy as np
import pandas as pd
from PEC_functions import predict, control, explain

# %%
# define functions
def get_trials_and_tasks(participant_id):
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


def calculate_probabilities(trials_vis, trials_hid, MM, task):
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

def compute_Ri(trials, task, form, epsilon, beta):
    import math
    log_p_answers = []
    for index in range(0, trials.shape[0]):
        option_1_p_mm = trials.iloc[[index]].option_1_p_mm.item()
        option_2_p_mm = trials.iloc[[index]].option_2_p_mm.item()
        response = trials.iloc[[index]].response.item()

        if task == "prediction":
            option_1 = int(trials.iloc[[index]].option_1.item())
            option_2 = int(trials.iloc[[index]].option_2.item())
        if task == "explanation":
            option_1 = 1
            option_2 = 2
        if task == "control":
            option_1 = trials.iloc[[index]].option_1.item() if form == "hidden" else "a"
            option_2 = trials.iloc[[index]].option_2.item() if form == "hidden" else "b"

        # R_i
        if option_1_p_mm > option_2_p_mm:
            R_i = math.log((option_1_p_mm + epsilon)/(option_2_p_mm + epsilon))
        elif option_1_p_mm < option_2_p_mm:
            R_i = math.log((option_2_p_mm + epsilon)/(option_1_p_mm + epsilon))
        else:
            R_i = 1

        p_correct = (math.e ** (R_i * beta)) / (math.e ** (R_i * beta) + math.e ** (-1 * R_i * beta))

        if task == "explanation":
            correct_mm = option_1 if option_1_p_mm < option_2_p_mm else option_2
        else: correct_mm = option_1 if option_1_p_mm > option_2_p_mm else option_2

        p_answer = p_correct if response == correct_mm else (1 - p_correct)
        log_p_answer = math.log(p_answer)
        log_p_answers.append(log_p_answer)
    return R_i, p_correct, p_answer, log_p_answers

# %%

# %%
sample = {}
for participant_id in trials_learning.participant_id.unique():

    # import mental model from csv file
    mm = transitions[transitions['participant_id'] == participant_id]

    # reformat mental model as dictionary
    MM = {}
    for state_current in mm.state_current.unique():
        inputs = {}
        for inp in ["a", "b"]:
            inputs[inp] = np.array([mm.state_next_p[(mm.state_current == state_current) & (mm.response_current == inp) & (mm.state_next == 0)].item(),
                                    mm.state_next_p[(mm.state_current == state_current) & (mm.response_current == inp) & (mm.state_next == 1)].item(),
                                    mm.state_next_p[(mm.state_current == state_current) & (mm.response_current == inp) & (mm.state_next == 2)].item(),
                                    mm.state_next_p[(mm.state_current == state_current) & (mm.response_current == inp) & (mm.state_next == 3)].item()])
        MM[state_current] = {"a":inputs["a"], "b": inputs["b"]}

    # import test trials from csv files and get task type
    trials_vis, trials_hid, task = get_trials_and_tasks(participant_id)

    # calculate probability of each option for each trial
    trials_vis, trials_hid = calculate_probabilities(trials_vis, trials_hid, MM, task)
    sample[participant_id] = trials_vis, trials_hid

    for index, row in trials_vis.iterrows():
        trials_vis.loc[index, 'R_i'] = compute_Ri(trials_vis, task, "visible", 0.0001, 1)[0]
        trials_vis.loc[index, 'p_correct'] = compute_Ri(trials_vis, task, "visible", 0.0001, 1)[1]
        trials_vis.loc[index, 'p_answer'] = compute_Ri(trials_vis, task, "visible", 0.0001, 1)[2]
        trials_vis.loc[index, 'log_p_answer'] = compute_Ri(trials_vis, task, "visible", 0.0001, 1)[3]

# calculate Ri for each trial

# export data to csv file: participant_id, fsm_type, trial_type, trial_number, Ri, response_correct

# %%
