import matplotlib.pyplot as plt
import seaborn as sns


iris_data = sns.load_dataset("iris")

sns.lmplot(x="sepal_length", y="sepal_width", hue="species", data=iris_data)

plt.show()
