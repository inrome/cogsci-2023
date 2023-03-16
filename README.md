
# Prediction, Explanation, and Control Under Free Exploration Learning: Experiment 1

# Requirements
- Data collection: [Lab.JS](https://lab.js.org/) + [Open Lab](https://open-lab.online/)
- Preprocessing: RStudio (R version 4.2.1)
- Main analysis: Python 3.7

## Procedure
The experiment consisted of **learning** and **test** phases followed by a post-experimental questionnaire.
- Learning phase (45 interactions): participants freely interacted with the chatbot so that they could explain, predict, and control its behavior. Participants respond by choosing one of the two emoji icons (corresponding to "a", or "b") and instantly get the next reaction of the chatbot, which depends on their input and the previous message from the chatbot.
- Test phase (20 questions — 10 hidden and 10 visible): Participants were randomly assigned to one of three test conditions that assessed their ability to predict, explain, or control the chatbot's behavior.
- Questionnaire: 1) _How many correct answers do you think you got in the test task?_ (multiple-choice question). 2) _How did you come up with most of the anwers during the test phase?_ (multiple-choice question). 3) _Imagine that your friend is taking part in the study and want to excel in the test task. What would you advise?_ (text input)

## Data analysis Python scripts
`0-import_data_from-csv.py` — imports data from preprocessed csv to the `imported_clean_data.pickle` file with 5 pandas DataFrames: 
- `participants` — rows are individual participants (n = 91) 
- `trials_learning` — rows are trials (4095 = 45×91) in the learning phase (interactions with the chatbot)
- `trials_prediction`, `trials_control`, `trials_explanation` — rows are trials for participants in the corresponding test condition (20 trials for each person)

`1_generate_mental_models.py` — generates `mental_models.pickle` containing a dictionary with probailities of transitions inferred from learning phase responses observed by each participant. For example, `fsm[1]['a']` would provide a list of probabilities for yeach of four possible next states for current state (1) followed by input 'a'.

Transitions that were not exproled in the learning phase are treated as transtions with equal probabilities for all of the four possible next states i.e., `[0.25, 0.25, 0.25, 0.25]` 

`PEC_functions.py` — three functions that calculate probabilities for all possible responses in prediction, explanation, and control test tasks for questions with hidden middle states

`2_calculate_PEC_probabilities.py` — generates `trials_with_PEC_mm.pickle` containing a dictionary participant IDs as keys and four nested dictionaries:
- `trials_vis` — trials (n = 10) with questions in visible form (i.e., middle state is known) and columns containing probabilities of aswer options (`option_1_p_mm` and `option_1_p_mm`) in Prediction, Explanation and Control tasks calculated based in participants' mental models 
- `trials_hid` — same, but with probabilites calculated with `PEC_functions.py` for question in the "hidden" form (with a hidden middle state). Additionaly has `option_1_p_mm_an` and `option_2_p_mm_an` with calculations under the alternative neglect assumption (the most likely middle state instead of sum over all possible middle states). 

`3_calculate_Ri.py` — computes R_i (a measure of difficulty of each question) for all trials in visible and hidden trials from `trials_with_PEC_mm.pickle` and saves to `trials_with_Ri.pickle`

`4_add_MM_accuracy` — updates `trials_with_Ri.pickle` to include accuracy based on mental models
- `response_correct_mm` — 1 if the response was correct based on mental model, 0 otherwise
- `response_correct_mm_an` — 1 if the response was correct based on mental model under the alternative neglect assumption, 0 otherwise

`4b_export_Ri_and_mm_accuracy.py` — takes `trials_with_Ri.pickle` and exports trials with Ri and mental model accuracy to `all_trials_with_Ri.csv`

`5_calculate_log_p_answer.py` — takes `trials_with_Ri.pickle` and `imported_clean_data.pickle` and calculates `max_beta`, `predicted_accuracy`, `mm_accuracy`, and `count_nan` variables for each participant. 
- Saves to `trials_with_max_beta.pickle`
- Exports to `predicted_accuracy.csv`

## Demo Experiment
You can try the [Chatbot Interaction Task v2](https://open-lab.online/test/interaction-with-a-chatbot-using-emoji-2/63d0229665c37c3fabb854cb) hosted at Open Lab

## Related Projects
[Prediction, Explanation, and Control Under Free Exploration Learning: Experiment 2](https://github.com/inrome/pec-preview)

## Screenshots of the experimental procedure
### Learningn phase:
![Learning Phase](https://github.com/inrome/cogsci-2023/blob/main/screenshots/1-1_learning_trial.png?raw=true) 

### Test phase:
![Test Phase](https://github.com/inrome/cogsci-2023/blob/main/screenshots/test_phase_screens.png?raw=true)
 
### Questionnaire:
![Q1](https://github.com/inrome/cogsci-2023/blob/main/screenshots/3-1_q_estimate.png?raw=true)
![Q2](https://github.com/inrome/cogsci-2023/blob/main/screenshots/3-2%20question%20strategy.png?raw=true)
![Q3](https://github.com/inrome/cogsci-2023/blob/main/screenshots/3-3%20question%20advice.png?raw=true)

## Authors
- Roman Tikhonov ([Google Scholar](https://scholar.google.ru/citations?user=4ag4R48AAAAJ&hl=ru))
- Simon DeDeo ([Google Scholar](https://scholar.google.com/citations?user=UW3tRn8AAAAJ&hl=en))
