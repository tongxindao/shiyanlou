import matplotlib.pyplot as plt
import seaborn as sns


iris_data = sns.load_dataset("iris")

sns.PairGrid(data=iris_data, hue="species").map(plt.scatter)
plt.show()
