import matplotlib.pyplot as plt
import seaborn as sns


iris_data = sns.load_dataset("iris")
iris_data.pop("species")

sns.clustermap(iris_data)
plt.show()
