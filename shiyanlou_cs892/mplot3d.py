from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


x = np.linspace(-6 * np.pi, 6 * np.pi, 1000)
y = np.sin(x)
z = np.cos(x)

fig = plt.figure()
ax = Axes3D(fig)

ax.plot(x, y, z)

plt.show()
