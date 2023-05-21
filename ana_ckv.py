#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/5/21 14:00
# @Author  : Tom SONG 
# @Mail    : xdmyssy@gmail.com
# @File    : ana_ckv.py
# @Software: PyCharm

import numpy as np

from read_root import ReadRoot

def get_cherenkov_signal(file_path):
    data=ReadRoot(file_path=file_path, tree_name='Calib_Hit', exp=['Cherenkov'])
    ckv=data.readBranch('Cherenkov')
    ckv=np.vstack(ckv)
    return ckv


def get_event_num(file_path):
    data = ReadRoot(file_path=file_path, tree_name='Calib_Hit', exp=['Event_Num'])
    e_num = data.readBranch('Event_Num')
    return e_num


def select_data(ahcal_file_path,ecal_file_path,save_path=None, use_ckv_info=False, statistics=-1):
    '''select pbar
    :return the slected event index'''

    e_event_num=get_event_num(ecal_file_path)
    a_event_num=get_event_num(ahcal_file_path)

    a_index = np.arange(len(a_event_num))
    e_index = np.arange(len(e_event_num))


    if use_ckv_info:
        ckv=get_cherenkov_signal(ahcal_file_path)

        p_bar_cut=np.logical_and(ckv[:,0]==0, ckv[:,1]==0)
        # picked event_num
        a_index=a_index[p_bar_cut]
        a_event_num=a_event_num[p_bar_cut]

    a_event_num=a_event_num+1 # considering shift=1

    assert len(a_index)==len(a_event_num)

    picked_index_pair=[]

    for ecal_index, ecal_event_num in zip(e_index, e_event_num):
        for ahcal_index, ahcal_event_num in zip(a_index, a_event_num):
            if ecal_event_num == ahcal_event_num:
                picked_index_pair.append([ecal_index,ahcal_index])
                break
            else:
                continue

        if statistics>0 and len(picked_index_pair)>statistics:
            break



    if save_path !=None:
        np.save(save_path,picked_index_pair)

        return

    return picked_index_pair

if __name__ == '__main__':

    select_data(ecal_file_path='/home/songsy/CEPCEventDisplay/data/mnt2/ScECAL/2023/Result_PS/calib/pi-/3GeV/ECAL_Run38_20230520_023458.root',
                ahcal_file_path='/home/songsy/CEPCEventDisplay/data/mnt2/AHCAL/PublicAna/2023/BeamAna/result/PS/pi-/3GeV/AHCAL_Run38_20230520_023441.root',
                save_path='/home/songsy/CEPC_2023TB/ahcal_ana/npy_file/run38.npy',
                use_ckv_info=False,
                statistics=100)

    pass
