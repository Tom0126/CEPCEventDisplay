

from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt

from matplotlib import cm

from matplotlib.ticker import LinearLocator, FormatStrFormatter

from ReadRoot import *
from DecodePosition import *

import numpy as np

fig = plt.figure(figsize=(10,10))

x_ahcal,y_ahcal,z_ahcal=getLocation('../Result/e/AHCAL_Run144_20221024_073230.root')
x_ahcal_positions, y_ahcal_positions, z_ahcal_positions = \
    -1 * x_ahcal[6], z_ahcal[6], y_ahcal[6]
ax = fig.gca(projection='3d')
plt.gca().set_box_aspect((1, 4, 1))
frame_unit = np.ones((2,2))
cell_alpha=1
for i in range(len(x_ahcal_positions)):

    x=x_ahcal_positions[i]
    y=y_ahcal_positions[i]
    z=z_ahcal_positions[i]
    x0,x1=x-20,x+20
    y0, y1 = y - 1.5, y + 1.5
    z0, z1 = z - 20, z + 20
    lch1 = np.array([x0, x1])
    lch2 = np.array([y0, y1])
    lch3 = np.array([z0, z1])
    hcf_xy, hcf_xz = np.meshgrid(lch2, lch3)  # AHCAL Face yz
    hcf_yx, hcf_yz = np.meshgrid(lch1, lch3)
    hcf_zx, hcf_zy = np.meshgrid(lch1, lch2)
    surf_xz0 = ax.plot_surface(hcf_yx, y0 * frame_unit, hcf_yz, alpha=0.8, linewidth=0.1,
                               antialiased=False, rstride=1,
                               cstride=1,
                               )

    surf_xz1 = ax.plot_surface(hcf_yx, y1 * frame_unit, hcf_yz, alpha=cell_alpha, linewidth=0.1,
                                           antialiased=False, rstride=1,
                                           cstride=1,
                                           )
    surf_xy0 = ax.plot_surface(hcf_zx, hcf_zy, z0 * frame_unit, alpha=cell_alpha, linewidth=0.1,
                               antialiased=False, rstride=1,
                               cstride=1,
                              )
    surf_xy1 = ax.plot_surface(hcf_zx, hcf_zy, z1*frame_unit, alpha=cell_alpha, linewidth=0.1,
                               antialiased=False, rstride=1,
                               cstride=1,
                               )
    surf_yz0 = ax.plot_surface(x0 * frame_unit, hcf_xy, hcf_xz, alpha=cell_alpha, linewidth=0.1,
                               antialiased=False, rstride=1,
                               cstride=1,
                               )
    surf_yz1 = ax.plot_surface(x1 * frame_unit, hcf_xy, hcf_xz, alpha=cell_alpha, linewidth=0.1,
                               antialiased=False, rstride=1,
                               cstride=1,
                               )
# scale = 19
#
# # Make data.
#
# X = np.arange(1, scale+1, 1)
#
# Z = np.arange(1, scale+1, 1)
#
# X, Z = np.meshgrid(X, Z)
#
# unit = np.ones(X.shape)
#
#
# # set facecolors
# colors=np.empty(X.shape,dtype='U50')
# for i in range(18):
#     for j in range(18):
#         colors[i,j]='green'
#
# # Plot the surface.


# for i in range(2):
#     color_layer=colors.copy()
#     # test
#     x_index=1
#     z_index=1
#
#     # randint [low, high)
#     # index cell number: 1,...18,
#     # x_index=np.random.randint(1,19)
#     # z_index=np.random.randint(1,19)
#
#     # define facecolor: z, x order. careful
#     color_layer[z_index-1,x_index-1]='red'
#     Y=unit*i
#
#     # set one small patch
#     x2 = np.arange(x_index, x_index+2)
#     z2 = np.arange(z_index, z_index+2)
#     x2, z2 = np.meshgrid(x2, z2)
#     y2 = np.ones(x2.shape)*i
#     surf = ax.plot_surface(X, Y, Z,alpha=0.05,linewidth=0.1, antialiased=False,rstride=1,cstride=1,facecolors=color_layer)
#     surf2 = ax.plot_surface(x2, y2, z2, alpha=1*2**(-i/20), linewidth=0.1, antialiased=False, rstride=1, cstride=1,color='red')
#

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