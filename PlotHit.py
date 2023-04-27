import numpy as np
import matplotlib.pyplot as plt
import uproot
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from DecodePosition import *
from HashSets import *
from ReadRoot import *
import argparse

#########  parameter  ##########
file_to_dispaly='../cosmic0812.root'
fig_name_to_save='test.png'
layers_num=18 # total sampling layers
scale = 19
################################

# pick entry
parser=argparse.ArgumentParser()
parser.add_argument("-e",'--entry',help="the nth entry",type=int)
args=parser.parse_args()

# cellIDs
cellIDs=readRootFileCellIDs(file_to_dispaly)
# layers,chips, memo_ids, channels shape (num(events), x)
layers, chips, memo_ids, channels=decodeCellIDs(cellIDs)

random_seed=args.entry

assert args.entry < len(layers)
###################################################################
fig = plt.figure(figsize=(5,5))

ax = fig.gca(projection='3d')
plt.gca().set_box_aspect((1, 2, 1))


# Make data.

X = np.arange(1, scale+1, 1)

Z = np.arange(1, scale+1, 1)

X, Z = np.meshgrid(X, Z)

unit = np.ones(X.shape)


# set facecolors

# Plot the surface.

for i in range(1,layers_num+1):

    Y=unit*i
    surf = ax.plot_surface(X, Y, Z, alpha=0.1, linewidth=0.1, antialiased=False, rstride=1, cstride=1,color='green')



assert len(layers[random_seed])==len(chips[random_seed])
assert len(layers[random_seed])==len(channels[random_seed])


x_poitions,y_positions=getPosition(chips[random_seed],channels[random_seed])

for i in range(len(layers[random_seed])):
    # plot hit
    x_index=x_poitions[i]
    z_index=y_positions[i]

    x2 = np.arange(x_index, x_index+2)
    z2 = np.arange(z_index, z_index+2)
    x2, z2 = np.meshgrid(x2, z2)

    y2 = np.ones(x2.shape)*(1+ layers[random_seed][i])

    surf2 = ax.plot_surface(x2, y2, z2, alpha=1*2**(-layers[random_seed][i]/20), linewidth=0.1, antialiased=False, rstride=1, cstride=1,color='red')


# Customize the z axis.

# ax.set_zlim(0, 4000)
#
# ax.zaxis.set_major_locator(LinearLocator(10))
#
# ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

# axis label
ax.set_ylabel('Layers', fontsize=20)
ax.set_yticks(np.arange(1,layers_num+1))
# rotate the axes and update

for angle in range(0, 360):
    # ideal direction: (30, -40)
    # test firection (0, -90)
    ax.view_init(30, -40)

# remove the background meshgrid
ax.grid(False)
plt.savefig(fig_name_to_save)
plt.show(block=False)
plt.pause(5)
plt.close()
