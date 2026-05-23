import seaborn as sns
import matplotlib.pyplot as plt

df = sns.load_dataset("iris")

sns.scatterplot(
    data=df,
    x="petal_length",
    y="petal_width",
    hue="species"
)

plt.show()