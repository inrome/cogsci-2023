
# Prediction, Explanation, and Control Under Free Exploration Learning: Experiment 1

# Requirements
- Data collection: [Lab.JS](https://lab.js.org/) + [Open Lab](https://open-lab.online/)
- Preprocessing: RStudio (R version 4.2.1)
- Main analysis: Python 3.7
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
## Demo Experiment
You can try the [Chatbot Interaction Task v2](https://open-lab.online/test/interaction-with-a-chatbot-using-emoji-2/63d0229665c37c3fabb854cb) hosted at Open Lab

## Related Projects
[Prediction, Explanation, and Control Under Free Exploration Learning: Experiment 2](https://github.com/inrome/pec-preview)


## Authors
- Roman Tikhonov ([Google Scholar](https://scholar.google.ru/citations?user=4ag4R48AAAAJ&hl=ru))
- Simon DeDeo ([Google Scholar](https://scholar.google.com/citations?user=UW3tRn8AAAAJ&hl=en))


## Screenshots of the experimental procedure
### Learningn phase:
![Learning Phase](https://github.com/inrome/cogsci-2023/blob/main/screenshots/1-1_learning_trial.png?raw=true) 

### Test phase:
![Test Phase](https://github.com/inrome/cogsci-2023/blob/main/screenshots/test_phase_screens.png?raw=true)
 
### Questionnaire:
![Q1](https://github.com/inrome/cogsci-2023/blob/main/screenshots/3-1_q_estimate.png?raw=true)
![Q2](https://github.com/inrome/cogsci-2023/blob/main/screenshots/3-2%20question%20strategy.png?raw=true)
![Q3](https://github.com/inrome/cogsci-2023/blob/main/screenshots/3-3%20question%20advice.png?raw=true)


