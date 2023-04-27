import numpy as np
from HashSets import *

if __name__ == '__main__':
    pos_info=np.loadtxt('Pos.txt')

    shape=pos_info.shape
    D={}
    for i in range(shape[0]):
        for j in range(shape[1]):
            D[int(pos_info[i,j])]=[shape[0]-1-i,shape[1]-1-j]

    saveHashSets('ids_postions.txt',D)