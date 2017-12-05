import matplotlib.pyplot as plt
import seaborn as sns


iris_data = sns.load_dataset("iris")

sns.JointGrid(data=iris_data, x="sepal_length", y="sepal_width").plot(sns.regplot, sns.distplot)
plt.show()
