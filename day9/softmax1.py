import numpy as np

scores = np.array([2, 1, 0])

exp_scores = np.exp(scores)

softmax = exp_scores / np.sum(exp_scores)

print(softmax)

# 출력 결과
# [0.66524096 0.24472847 0.09003057]

