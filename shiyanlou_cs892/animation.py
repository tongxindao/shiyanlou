#_*_ coding: utf-8 _*_
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


fig, ax = plt.subplots()
x = np.arange(0, 2 * np.pi, 0.01)
line, = plt.plot(x, np.sin(x))

def update(i):
    line.set_ydata(np.sin(x + i / 10.0))
    return line

animation = animation.FuncAnimation(fig, update)

plt.show()
