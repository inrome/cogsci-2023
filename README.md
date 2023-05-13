
# Prediction, Explanation, and Control Under Free Exploration Learning: Experiment 1

# Requirements
- Data collection: [Lab.JS](https://lab.js.org/) + [Open Lab](https://open-lab.online/)
- Python 3.11.2

## Procedure
The experiment consisted of **learning** and **test** phases followed by a post-experimental questionnaire.
- Learning phase (45 interactions): participants freely interacted with the chatbot with a goal defined in general terms (to be able to explain, predict, and control the chatbot's behavior). Participants respond by choosing one of the two emoji icons (corresponding to "a", or "b") and instantly get the next reaction of the chatbot (emoji assigned to states 0, 1, 2, or 3), which depends on their input and the previous message from the chatbot.
Chatbot's behavior was defined with either "**easy**" or "**hard**" finite-state machine that differed in the number of deterministic or probabilistic transitions.
- Test phase (20 questions — 10 hidden and 10 visible): Participants were randomly assigned to one of three test conditions that assessed their ability to predict, explain, or control the chatbot's behavior.
- Questionnaire: 1) _How many correct answers do you think you got in the test task?_ (multiple-choice question). 2) _How did you come up with most of the anwers during the test phase?_ (multiple-choice question). 3) _Imagine that your friend is taking part in the study and want to excel in the test task. What would you advise?_ (text input)

## Demo Experiment
You can try the [Chatbot Interaction Task v2](https://open-lab.online/test/interaction-with-a-chatbot-using-emoji-2/63d0229665c37c3fabb854cb) hosted at Open Lab


## Components

### Lab.JS
`materials/chatbot_v2_free_exploration.json` — Lab.JS program for data collection. See the platform's documentation: https://labjs.readthedocs.io/


### Data
`data/` — preprocessed data from the experiment as csv and a pickle file with a dictionary of pandas DataFrames
- `imported_clean_data.pickle` file with 5 pandas DataFrames: 
    - `participants` — rows are individual participants (n = 97) 
    - `trials_learning` — rows are trials in the learning phase (interactions with the chatbot)
    - `trials_prediction`, `trials_control`, `trials_explanation` — rows are trials for participants in the corresponding test condition (20 trials for each person)
- csv files with the same dataframes 

## Data analysis Python scripts
Folder `scripts_python/` contains Python scripts for data analysis: 

`1-mental_models.py` — generates `outputs/mental_models.pickle` containing a dictionary with probailities of transitions inferred from learning phase responses observed by each participant. For example, `fsm[1]['a']` would provide a list of probabilities for yeach of four possible next states for current state (1) followed by input 'a'. 

Transitions that were not exproled in the learning phase are treated as transtions with equal probabilities for all of the four possible next states i.e., `[0.25, 0.25, 0.25, 0.25]` 

`PEC_functions.py` — three functions that calculate probabilities for all possible responses in prediction, explanation, and control test tasks for questions with hidden middle states

`2_add_PEC_probabilities.py` — generates `trials_with_PEC_mm.pickle` containing a dictionary participant IDs as keys and four nested dictionaries:
- `trials_vis` — trials (n = 10) with questions in visible form (i.e., middle state is known) and columns containing probabilities of aswer options (`option_1_p_mm` and `option_1_p_mm`) in Prediction, Explanation and Control tasks calculated based in participants' mental models 
- `trials_hid` — same, but with probabilites calculated with `PEC_functions.py` for question in the "hidden" form (with a hidden middle state). Additionaly has `option_1_p_mm_an` and `option_2_p_mm_an` with calculations under the alternative neglect assumption (the most likely middle state instead of sum over all possible middle states). 

`3_calculate_Ri.py` — computes R_i (a measure of difficulty of each question) for all trials in visible and hidden trials from `trials_with_PEC_mm.pickle` and saves to `trials_with_Ri.pickle`

`4_add_MM_accuracy` — updates `trials_with_Ri.pickle` to include accuracy based on mental models
- `response_correct_mm` — 1 if the response was correct based on mental model, 0 otherwise
- `response_correct_mm_an` — 1 if the response was correct based on mental model under the alternative neglect assumption, 0 otherwise

`5_export_csv_with_Ri_and_accuracy.py` — takes `trials_with_Ri.pickle` and exports trials with Ri and mental model accuracy to `all_trials_with_Ri.csv`

`6_calculate_log_p_answer.py` — takes `trials_with_Ri.pickle` and `imported_clean_data.pickle` and calculates `max_beta`, `predicted_accuracy`, `mm_accuracy`, and `count_nan` variables for each participant. 
- Saves to `trials_with_max_beta.pickle`
Additionally, fits beta for all trials in each condition and calculates 95% confidence intervals and saves to `outputs/beta_with_plus_minus_2LL_errors.csv`

`scripts_python/7_stats_and_plots.ipynb` — Jupyter notebook with statistical analysis and plots.

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
