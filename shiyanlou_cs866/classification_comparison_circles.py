# -*- coding: utf-8 -*

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.datasets import make_circles

# 集成方法分类器
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier

# 高斯过程分类器
from sklearn.gaussian_process import GaussianProcessClassifier

# 广义线性分类器
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.linear_model import RidgeClassifier
from sklearn.linear_model import SGDClassifier

# K近邻分类器
from sklearn.neighbors import KNeighborsClassifier

# 朴素贝叶斯分类器
from sklearn.naive_bayes import GaussianNB

# 神经网络分类器
from sklearn.neural_network import MLPClassifier

# 决策树分类器
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import ExtraTreeClassifier

# 支持向量机分类器
from sklearn.svm import SVC
from sklearn.svm import LinearSVC

classifier_Names = ['AdaBoost', 'Bagging', 'ExtraTrees', 'GradientBoosting', 'RandomForest',
                    'GaussianProcess', 'PassiveAggressive', 'Ridge', 'SGD',
                    'KNeighbors', 'GaussianNB', 'MLP', 'DecisionTree', 'ExtraTree', 'SVC',
                    'LinearSVC']
model = [
    AdaBoostClassifier(),
    BaggingClassifier(),
    ExtraTreesClassifier(),
    GradientBoostingClassifier(),
    RandomForestClassifier(),
    GaussianProcessClassifier(),
    PassiveAggressiveClassifier(),
    RidgeClassifier(),
    SGDClassifier(),
    KNeighborsClassifier(),
    GaussianNB(),
    MLPClassifier(),
    DecisionTreeClassifier(),
    ExtraTreeClassifier(),
    SVC(),
    LinearSVC()
]

# 读取数据并切分
data = pd.read_csv("data_circles.csv", header=0)


feature = data[['X', 'Y']]
target = data['CLASS']
X_train, X_test, y_train, y_test = train_test_split(feature, target, test_size=.3)

# 绘制数据集
i = 1
cm = plt.cm.Reds
cm_color = ListedColormap(['red', 'yellow'])

x_min, x_max = data['X'].min() - .5, data['X'].max() + .5
y_min, y_max = data['Y'].min() - .5, data['Y'].max() + .5

xx, yy = np.meshgrid(np.arange(x_min, x_max, .1),
                     np.arange(y_min, y_max, .1))

# 模型迭代
for name, clf in zip(classifier_Names, model):
    ax = plt.subplot(4, 4, i)

    clf.fit(X_train, y_train)
    pre_labels = clf.predict(X_test)
    score = accuracy_score(y_test, pre_labels)

    if hasattr(clf, "decision_function"):
        Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
    else:
        Z = clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]

    Z = Z.reshape(xx.shape)
    ax.contourf(xx, yy, Z, cmap=cm, alpha=.6)

    ax.scatter(X_train['X'], X_train['Y'], c=y_train, cmap=cm_color)
    ax.scatter(X_test['X'], X_test['Y'], c=y_test, cmap=cm_color, edgecolors='black')

    ax.set_xlim(xx.min(), xx.max())
    ax.set_ylim(yy.min(), yy.max())
    ax.set_xticks(())
    ax.set_yticks(())
    ax.set_title('%s | %.2f' % (name, score))

    i += 1

plt.show()