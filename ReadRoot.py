import uproot
import os
import datetime
import time
import numpy as np


def readRootFileCellIDs(path):
    file = uproot.open(path)

    event = file['Calib_Hit']


    # Get data->numpy
    data = event.arrays(library="np")
    # cellIDs
    cellIDs = data['CellID']

    return cellIDs


def readRootFileTimes(path):
    file = uproot.open(path)


    event = file['Calib_Hit']

    # Get data->numpy
    data = event.arrays(library="np")
    # cellIDs
    times = data['Hit_Energy']
    return times


def readRootFileE(path):
    file = uproot.open(path)
    # get keys
    # print(file.keys())
    # A TTree File
    event = file['Calib_Hit']
    # Get data->numpy
    data = event.arrays(library="np")
    # cellIDs
    energies = data['Hit_Energy']
    return energies


def readRootFileHitTags(path):
    file = uproot.open(path)

    event = file['Calib_Hit']

    # Get data->numpy
    data = event.arrays(library="np")
    # cellIDs
    hitTags = data['HitTag']
    return hitTags


def pickTriggerIDEntry(triggerIDs):
    picked_entries = [0]
    length = len(triggerIDs)
    if length < 1:
        return []
    point = 1
    while point < length:
        if triggerIDs[point] != triggerIDs[point - 1]:
            picked_entries.append(point)
        point += 1
    return picked_entries


def getTriggerID(path):
    '''before calib: choose ahcal or not
       after calib: choose calib or not
    '''
    file = uproot.open(path)

    event = file['Calib_Hit']

    # Get data->numpy
    data = event.arrays(library="np")
    triggerID = data['Event_Num']
    return triggerID

def getHit_X(path):
    '''before calib: choose ahcal or not
       after calib: choose calib or not
    '''
    file = uproot.open(path)

    event = file['Calib_Hit']

    # Get data->numpy
    data = event.arrays(library="np")
    Hit_X = data['Hit_X']
    return Hit_X

def getHit_Y(path):
    '''before calib: choose ahcal or not
       after calib: choose calib or not
    '''
    file = uproot.open(path)

    event = file['Calib_Hit']

    # Get data->numpy
    data = event.arrays(library="np")
    Hit_Y = data['Hit_Y']
    return Hit_Y

def getLocation(path, calib=True):
    file = uproot.open(path)
    if calib:
        event = file['Calib_Hit']
        # Get data->numpy
        data = event.arrays(library="np")
        hit_x = data['Hit_X']
        hit_y = data['Hit_Y']
        hit_z = data['Hit_Z']
        # z: incident particle direction
        return hit_x, hit_y, hit_z
    else:
        print('Not calibrated')


def getLatestRootFile(dir):
    '''MacOS form'''
    # list files in a path
    lists = os.listdir(dir)
    lists = list(filter(file_filter, lists))
    # in time order
    lists.sort(key=lambda fn: os.path.getmtime(dir + '/' + fn))
    # get latest data
    filetime = datetime.datetime.fromtimestamp(os.path.getmtime(dir + '/' + lists[-1]))
    # get file's dir
    filepath = os.path.join(dir, lists[-1])
    # print("The latest file：" + lists[-1])
    # print("Time：" + filetime.strftime('%Y-%m-%d %H-%M-%S'))
    return filepath


def file_filter(f):
    if f[-5:] in ['.root']:
        return True
    else:
        return False


def readRootFileCellIDsTest(path, ahcal=True):
    file = uproot.open(path)
    # get keys
    if ahcal:
        event = file['Cosmic Event']
    else:
        event = file['T_Event']
    # Get data->numpy

    cellIDs = event.arrays(['cellIDs'], cut='hitTags==1', library='np', aliases={"hitTags": "hitTags"})

    return cellIDs


if __name__ == '__main__':
    # np.set_printoptions(threshold=np.inf)
    # triggerIDs = getTriggerID('../Result/ECAL/xaa.root',ahcal=False)
    # print(triggerIDs.astype(np.int32))
    energies = readRootFileE('../Result/e/AHCAL_Run144_20221024_073230.root')

    # x,y,z=getLocation('../Result/e/AHCAL_Run144_20221024_073230.root')
    # x_ahcal_positions, y_ahcal_positions, z_ahcal_positions = \
    #     -1 * x[6], z[6], y[6]
    # print(x_ahcal_positions,y_ahcal_positions,z_ahcal_positions)
    # print(len(x_ahcal_positions), len(y_ahcal_positions), len(z_ahcal_positions))

    # picked_entries = pickTriggerIDEntry(triggerIDs)
    # print(picked_entries)
    # print(energies)
    print(np.min(energies[6]),np.max(energies[6]))