import numpy as np
import matplotlib.pyplot as plt
import uproot
from HashSets import *
from ReadRoot import *
import os


def decodeCellIDs(cellIDs):
    '''
    layer: AHCAL 0-39, ECAL 0-31.
    chip: AHCAL 0-6, ECAL 0-8
    channels: AHCAL，ECAL 0-35
    :param cellIDs:
    :return:
    '''

    scale = 100000

    layers = cellIDs // scale
    chips = (cellIDs - scale * layers) // 10000
    memo_ids = (cellIDs - scale * layers - 10000 * chips) // 100
    channels = cellIDs % 100
    return layers, chips, memo_ids, channels


def getAHCALPosition(hit_x, hit_y):
    '''1: chips, channels: lists
       2: start (1,18)
       3: AHCAL'''


    assert len(hit_x) == len(hit_y)

    hit_x = np.around(((hit_x + 342.5491) / 40.29964)+1).astype(int)
    hit_y = np.around(((hit_y + 343.05494) / 40.29964)+1).astype(int)

    hit_x=np.where(np.logical_or(hit_x>18,hit_x<1), -1, hit_x)
    hit_y = np.where(np.logical_or(hit_y > 18, hit_y < 1), -1, hit_y)
    return hit_x, hit_y


def getECALPosition(layers, chips, channels):
    '''1: chips, channels: lists
       2: start (1,18)
       3: ECAL'''
    decode_ids = np.array(
        [0, 42, 1, 43, 2, 44, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 54, 13, 55, 14, 56, 15, 57, 16, 58, 17, 59, 18, 60, 19,
         61, 20, 62, 21, 22, 23,
         24, 66, 25, 67, 26, 68, 27, 69, 28, 70, 29, 71, 30, 72, 31, 73, 32, 74, 33, 75, 34, 76, 35, 77, 36, 78, 37, 79,
         38, 80, 39,
         81, 40, 82, 41, 83, 149, 148, 147, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 63, 64, 65, 108,
         109, 110,
         111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 150, 192, 151, 193, 152, 194, 153,
         195,
         154, 196, 155, 197, 156, 198, 157, 199, 158, 200, 159, 201, 160, 202, 161, 203, 162, 204, 163, 205, 164, 206,
         165, 207,
         166, 208, 167, 209, 191, 190, 189, 188, 146, 187, 145, 186, 144, 185, 143, 184, 142, 183, 141, 182, 140, 181,
         139, 180,
         138, 179, 178, 177, 176, 175, 174, 173, 172, 171, 170, 128, 169, 127, 168, 126, 137, 136, 135, 134, 133, 132,
         131, 130,
         129, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 45, 46, 47, 48, 49, 50, 51, 52, 53, 210, 210, 210, 210,
         210, 210]) \
        .reshape(6, 36)
    x1_positions = []
    x2_positions = []
    x3_positions = []
    x1_interval = 5.3
    x2_interval = 45.4
    row_num = 42
    col_num = 5
    length = len(chips)
    assert len(channels) == len(chips)
    assert len(channels) == len(layers)

    for i in range(length):
        if chips[i]>-1 and chips[i] < 6 and channels[i]>-1 and channels[i]<36:
            scin_id = decode_ids[chips[i], channels[i]]
            layer_id = layers[i]
            x1_id = scin_id % row_num
            x2_id = scin_id // row_num
            x1 = x1_interval * x1_id - x1_interval * (row_num - 1) / 2.
            x2 = x2_interval * x2_id - x2_interval * (col_num - 1) / 2.
# TODO  modify codes after updating root files
            if layer_id % 2 == 0:
                # x1_positions.append(- x2)
                # x2_positions.append(-x1)
                _x1=int((2.65 + x1) / x1_interval + 20)
                _x2=int((-x2) / x2_interval + 2)
                if (_x1>-1) and (_x1<42) and (_x2>-1) and (_x2<5) and (layer_id>-1) and (layer_id<32): # remove faults
                    x1_positions.append(_x1)  # normalize the position:0,1,2...
                    x2_positions.append(_x2)
                else:
                    x1_positions.append(-1)
                    x2_positions.append(-1)
            else:
                # x1_positions.append(- x1)
                # x2_positions.append(-x2)
                _x1=int((x2) / x2_interval + 2)
                _x2=int((2.65 - x1) / x1_interval + 20)
                if (_x1 > -1) and (_x1 < 5) and (_x2 > -1) and (_x2 < 42)and (layer_id>-1) and (layer_id<32):  # remove faults
                    x1_positions.append(_x1)  # normalize the position:0,1,2...
                    x2_positions.append(_x2)
                else:
                    x1_positions.append(-1)
                    x2_positions.append(-1)
        else:
            x1_positions.append(-1)
            x2_positions.append(-1)
    return x1_positions, x2_positions


if __name__ == '__main__':
    # AHCAL
    # file = uproot.open("../cosmic.root")
    #
    # # A TTree File
    # cosmic_event = file['Cosmic Event']
    #
    # # Get data->numpy
    # data = cosmic_event.arrays(library="np")
    #
    # # cellIDs
    # cellIDs = data['cellIDs']

    # x_postions=np.array([100.2411,100.2411,100.2411,59.94146,59.94146,59.94146,19.64182,19.64182,19.64182,19.64182,
    #                      59.94146,100.2411,100.2411,59.94146,19.64182,100.2411,59.94146,19.64182,-20.65782,-60.95746,
    #                      -101.2571,-20.65782,-60.95746,-101.2571,-101.2571,-60.95746,-20.65782,-20.65782,-20.65782,-20.65782,
    #                      -60.95746,-60.95746,-60.95746,-101.2571,-101.2571,-101.2571])
    # y_positions=np.array([141.04874,181.34838,221.64802,141.04874,181.34838,221.64802,141.04874,181.34838,
    #                       221.64802,261.94766,261.94766,261.94766,302.2473,302.2473,302.2473,342.54694,
    #                       342.54694,342.54694,342.54694,342.54694,342.54694,302.2473,302.2473,302.2473,
    #                       261.94766,261.94766,261.94766,221.64802,181.34838,141.04874,221.64802,181.34838,
    #                       141.04874,221.64802,181.34838,141.04874])
    # x_postions=x_postions//35+3
    # y_positions=y_positions//40-3

    ####################
    #  chips
    #  1 4 7
    #  2 5 8
    #  3 6 9
    # init posiition (1, 18)
    #
    # D = readHashSets('ids_postions.txt')
    #
    # layers, chips, memo_ids, channels = decodeCellIDs(cellIDs)
    # # print(channels)

    # ECAL
    cellIDs = readRootFileCellIDs('../Result/ECAL/ECAL_Run222_20221027_224228.root')
    layers, chips, memo_ids, channels=decodeCellIDs(cellIDs)
    tags=readRootFileHitTags('../Result/ECAL/ECAL_Run222_20221027_224228.root')
    for i in range(20):
        l1=len(layers[i])
        _=[]
        for j in range(l1):
            if tags[i][j]==1:
                _.append(layers[i][j])
        print(_)
    x1s=[]
    x2s=[]
    x3s = []
    x4s = []
    num=len(cellIDs)

    # for index in range(num):
    #
    #     x1,x2=getECALPosition(layers[index],chips[index],channels[index],tags[index])
    #     length=len(layers[index])

    #     for i in range(length):
    #
    #         if layers[index][i]%2==0:
    #             # print(layers[index][i])
    #             if  x1[i] not in x1s:
    #                 x1s.append(x1[i])
    #             if  x2[i] not in x2s:
    #                 x2s.append(x2[i])
    #
    #             # print('x1:', x1[i],'x2:', x2[i])
    #
    #             # assert (x1[i]>-1) and (x1[i]<42)
    #             # assert (x2[i] > -1) and (x2[i] < 5)
    #         if layers[index][i] % 2 == 1:
    #             if x1[i] not in x3s:
    #                 x3s.append(x1[i])
    #             if x2[i] not in x4s:
    #                 x4s.append(x2[i])
    #             # print('x1:' ,x1[i])
    #             # print('x2:', x2[i])
    #             # assert (x2[i] > -1) and (x2[i] < 42)
    #             # assert (x1[i] > -1) and (x1[i] < 5)
    #         # print('x1:', x1[i], 'x2:', x2[i])
    # print(sorted(x1s))
    # print(sorted(x2s))
    # print(sorted(x3s))
    # print(sorted(x4s))



