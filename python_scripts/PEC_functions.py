import numpy as np

def predict(start_state, first_input, second_input, fsm_temp, mode="normative"):
    """Return an array with probabilities of each final state. E.g.: [0.4, 0.6, 0, 0].
    Higher probability = correct prediction."""
    states = [0, 1, 2, 3]
    if mode == "normative":
        return np.array([np.array([fsm_temp[start_state][first_input][middle_state] *
                                   fsm_temp[middle_state][second_input][final_state]
                                   for middle_state in states]).sum()
                         for final_state in states],
                        dtype=[(f"{start_state}—{first_input}–[All paths]–{second_input}–?", "float16")])
    elif mode == "an":
        max_middle_state = np.array([fsm_temp[start_state][first_input]]).argmax()
        ans = np.array([np.array([fsm_temp[middle_state][second_input][final_state]
                                  for middle_state in [max_middle_state]]).sum()
                        for final_state in states])
        return np.array(ans / ans.sum(),
                        dtype=[(f"{start_state}—{first_input}–[ML path]–{second_input}–?", "float16")])


def control(start_state, final_state, fsm_temp, mode="normative"):
    """ Returns a dictionary with input combinations (e.g., "ab" as keys) and probabilities of the outcome as values. Higher probability = correct control action.
    mode = "normative" calculates probabilities of each possible combination of inputs for every possible middle state.
    mode = "an" does the same, but only for the most probable middle state(s)
    """
    input_combinations = [["a", "a"], ["a", "b"], ["b", "a"], ["b", "b"]]
    states = [0, 1, 2, 3]
    control_result = {}
    for inp in input_combinations:
        label = inp[0] + inp[1]
        if mode == "normative":
            control_result[label] = np.array([fsm_temp[start_state][inp[0]][middle_state] *
                                              fsm_temp[middle_state][inp[1]][final_state] for middle_state in
                                              states]).sum()
        elif mode == "an":
            max_middle_state = np.array([fsm_temp[start_state][inp[0]]]).argmax()
            control_result[label] = np.array(
                [fsm_temp[middle_state][inp[1]][final_state] for middle_state in [max_middle_state]]).sum()
    return control_result


def explain(start_state, first_input, second_input, final_state, fsm_temp, mode="normative"):
    ''' Returns a dictionary with probabilities of the outcome under counterfactual reasoning. LOWER probability = correct explanation.
    ["1"] — probability of the outcome with a counterfactual first input.
    ["2"] — same, but with counterfactual second input'''
    ans = {}
    states = [0, 1, 2, 3]

    # first input counterfactual
    first_input_cf = "b" if first_input == "a" else "a"  # counteractual input 1

    # second input counterfactual
    second_input_cf = "b" if second_input == "a" else "a"  # counteractual input 2

    if mode == "normative":
        explanation_1 = np.array(
            [fsm_temp[start_state][first_input_cf][middle_state] * fsm_temp[middle_state][second_input][final_state]
             for middle_state in states]).sum()
        explanation_2 = np.array(
            [fsm_temp[start_state][first_input][middle_state] * fsm_temp[middle_state][second_input_cf][final_state]
             for middle_state in states]).sum()
    elif mode == "an":
        max_middle_state1 = np.array([fsm_temp[start_state][first_input_cf]]).argmax()
        max_middle_state2 = np.array([fsm_temp[start_state][first_input]]).argmax()
        explanation_1 = np.array(
            [fsm_temp[middle_state][second_input][final_state] for middle_state in [max_middle_state1]]).sum()
        explanation_2 = np.array(
            [fsm_temp[middle_state][second_input_cf][final_state] for middle_state in [max_middle_state2]]).sum()
    else:
        explanation_1 = None
        explanation_2 = None
    ans["1"] = explanation_1
    ans["2"] = explanation_2

    return ans

#%%
