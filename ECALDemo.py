

from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt

from matplotlib import cm

from matplotlib.ticker import LinearLocator, FormatStrFormatter

import numpy as np

fig = plt.figure(figsize=(10,10))

ax = fig.gca(projection='3d')
plt.gca().set_box_aspect((1, 4, 1))

start=1
end=1.1
step=0.1

Y_interval1 = 19.9
Y_interval2=11.2
x1_interval=5
x2_interval=42
# Make data.

XE = np.arange(0, x1_interval*43, x1_interval)
ZE = np.arange(0, x2_interval*6, x2_interval)
XE, ZE = np.meshgrid(XE, ZE)
unitE = np.ones((6,43))

ZO = np.arange(0, x1_interval * 43, x1_interval)
XO = np.arange(0, x2_interval * 6, x2_interval)
XO, ZO = np.meshgrid(XO, ZO)
unitO = np.ones((43, 6))

for i in range(32):
    # EBU
    if i % 2 == 0:
        Y = unitE * (1 + i // 2 * 19.9 - 19.9 * 16)
        X=XE
        Z=ZE
    else:
        Y = unitO * (12.2 + (i - 1) // 2 * 19.9  -19.9 * 16)
        X = XO
        Z = ZO
    surf = ax.plot_surface(X, Y, Z,alpha=0.2,linewidth=2)

layer_index=31
x_index = 4
z_index = 36
if layer_index % 2 == 0:
    x2 = np.arange(x_index * x1_interval, (x_index + 2) * x1_interval, x1_interval)
    z2 = np.arange(z_index * x2_interval, (z_index + 2) * x2_interval, x2_interval)
    x2, z2 = np.meshgrid(x2, z2)
    y2 = np.ones((2, 2)) * (1 + layer_index // 2 * 19.9 - 19.9 * 16)
    surf2 = ax.plot_surface(x2, y2, z2, alpha=0.8, linewidth=0.1,
                            antialiased=False, rstride=1, cstride=1,
                            )
else:
    x2 = np.arange(x_index * x2_interval, (x_index + 2) *x2_interval, x2_interval)
    z2 = np.arange(z_index * x1_interval, (z_index + 2) * x1_interval, x1_interval)
    x2, z2 = np.meshgrid(x2, z2)
    y2 = np.ones((2, 2)) * (12.2 + (layer_index - 1) // 2 * 19.9 - 19.9 * 16)
    surf2 = ax.plot_surface(x2, y2, z2, alpha=0.8, linewidth=0.1,
                            antialiased=False, rstride=1, cstride=1,
                            )

# Customize the z axis.

# ax.set_zlim(0, 4000)
#
# ax.zaxis.set_major_locator(LinearLocator(10))
#
# ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# rotate the axes and update

for angle in range(0, 360):
    # ideal direction: (30, -40)
    # test firection (0, -90)
    ax.view_init(0, -90)

# remove the background meshgrid
ax.grid(False)

plt.show()
plt.clf()