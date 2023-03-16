import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read and preprocess the data
ss_betas = pd.read_csv("../outputs/predicted_accuracy.csv")
ss_betas = ss_betas.rename(columns={"fsm": "difficulty", "condition": "visibility"})
ss_betas["task"] = ss_betas["task"].replace({"prediction": "Prediction", "control": "Control", "explanation": "Explanation"})
ss_betas["difficulty"] = ss_betas["difficulty"].replace({"easy": "Easy", "hard": "Hard"})
ss_betas["visibility"] = ss_betas["visibility"].replace({"visible": "Visible", "hidden": "Hidden", "hidden_an": "Hidden AN"})
ss_betas["difficulty"] = pd.Categorical(ss_betas["difficulty"], categories=["Easy", "Hard"], ordered=True)

# Create the boxplot
sns.set(style="whitegrid", font_scale=1.2)
palette = {"Prediction": "#AA4499", "Control": "#999933", "Explanation": "#6699CC"}
g = sns.catplot(data=ss_betas, x="task", y="predicted_accuracy", hue="task", col="difficulty", row="visibility",
                kind="box", dodge=True, width=0.5, fliersize=0, palette=palette, legend=False)

# Add jittered points
for ax in g.axes.flat:
    ax.axhline(0.5, color="black", linewidth=1, alpha=0.3)
    sns.stripplot(data=ss_betas, x="task", y="predicted_accuracy", hue="task", ax=ax, dodge=True, jitter=0.2, size=4,
                  alpha=0.2, linewidth=0, palette=palette, legend=False)

    # Set y-axis limits from 0 to 1
    ax.set_ylim(0.45, 1)

# Customize plot
g.set_axis_labels("Test condition", "Predicted Accuracy")
g.set_titles(col_template="{col_name}", row_template="{row_name}")

g.despine(left=True)

plt.savefig("../outputs/predicted_accuracy_alpha0.png", dpi=300, bbox_inches="tight")
plt.show()