import numpy as np
from HashSets import *
from ReadRoot import *
from DecodePosition import *
import matplotlib.pyplot as plt
import time
import os
# x_postions=np.array([100.2411,100.2411,100.2411,59.94146,59.94146,59.94146,19.64182,19.64182,19.64182,19.64182,
#                      59.94146,100.2411,100.2411,59.94146,19.64182,100.2411,59.94146,19.64182,-20.65782,-60.95746,
#                      -101.2571,-20.65782,-60.95746,-101.2571,-101.2571,-60.95746,-20.65782,-20.65782,-20.65782,-20.65782,
#                      -60.95746,-60.95746,-60.95746,-101.2571,-101.2571,-101.2571])
# y_positions=np.array([141.04874,181.34838,221.64802,141.04874,181.34838,221.64802,141.04874,181.34838,
#                       221.64802,261.94766,261.94766,261.94766,302.2473,302.2473,302.2473,342.54694,
#                       342.54694,342.54694,342.54694,342.54694,342.54694,302.2473,302.2473,302.2473,
#                       261.94766,261.94766,261.94766,221.64802,181.34838,141.04874,221.64802,181.34838,
#                       141.04874,221.64802,181.34838,141.04874])
# print(len(x_postions))
# x_postions=x_postions//35+3
# y_positions=y_positions//40-3
#
# positions=zip(x_postions,y_positions)
#
# id_posi_maps={}
# for i in range(36):
#     # id_posi_maps[i]=int(10*x_postions[i]+y_positions[i])
#     id_posi_maps[i] = [int(x_postions[i]) ,int(y_positions[i])]
# print(id_posi_maps)
# saveHashSets('ids_postions.txt',id_posi_maps)
# D2=readHashSets('ids_postions.txt')

# cellIDs=readRootFileCellIDs('../Result/20220911_162641.root')
# # layers,chips, memo_ids, channels shape (num(events), x)
# layers, chips, memo_ids, channels=decodeCellIDs(cellIDs)
# print(layers[-1])
# print(layers)
# hit_layers_nums=[]
# for layer in layers:
#     hit_layers_nums.append(len(layer))
# # print(nums)
# plt.hist(hit_layers_nums,bins=18,range=(0.5,18.5))
# plt.title('HitLayersNumbers')
# plt.xticks(np.arange(1,19))
# plt.show()
#
if __name__ == '__main__':
    label=r'$\frac'+'{\%}{\sqrt{E}}\oplus3\%$'
    plt.plot([1 for i in range(10)],[1 for i in range(10)],label=label )
    plt.legend()
    plt.show()