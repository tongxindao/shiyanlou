import matplotlib.pyplot as plt
import seaborn as sns


iris_data = sns.load_dataset("iris")

sns.kdeplot(data=iris_data["sepal_length"], data2=iris_data["sepal_width"], shade=True)
plt.show()
