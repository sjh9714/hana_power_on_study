import numpy as np

scores = np.array([3,4,6])

exp_scores = np.exp(scores)

attention_weights = exp_scores / np.sum(exp_scores)

print(attention_weights)