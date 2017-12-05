from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


fig = plt.figure()

ax1 = fig.add_subplot(1, 2, 1, projection="3d")

x = np.linspace(-6 * np.pi, 6 * np.pi, 1000)
y = np.sin(x)
z = np.cos(x)

ax1.plot(x, y, z)

ax2 = fig.add_subplot(1, 2, 2, projection="3d")

X = np.arange(-2, 2, 0.1)
Y = np.arange(-2, 2, 0.1)
X, Y = np.meshgrid(X, Y)
Z = np.sqrt(X ** 2 + Y ** 2)

ax2.plot_surface(X, Y, Z, cmap=plt.cm.winter)

plt.show()
