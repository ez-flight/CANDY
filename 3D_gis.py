import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
x = [1, 3, 5, 8, 6, 7, 1, 2, 4, 5]
y = [3, 4, 3, 6, 5, 3, 1, 2, 3, 8]

hist, xedges, yedges = np.histogram2d(x, y, bins=(4,4))
xpos, ypos = np.meshgrid(xedges[:-1]+xedges[1:], yedges[:-1]+yedges[1:])

xpos = xpos.flatten()/2.
ypos = ypos.flatten()/2.
zpos = np.zeros_like (xpos)

dx = xedges [1] - xedges [0]
dy = yedges [1] - yedges [0]
dz = hist.flatten()

ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='b', zsort='average')
plt.xlabel ("X")
plt.ylabel ("Y")

plt.show()