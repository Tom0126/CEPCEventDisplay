import numpy as np
import matplotlib.pyplot as plt
import uproot
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from DecodePosition import *
from HashSets import *
from ReadRoot import *
import tkinter as tk
import time

# In this version, only read valid triggerIDs

#########  parameter  ##########

file_to_dispaly = '../Result/HCAL_cosmic.root'


# fig_name_to_save = 'test.png'
# layers_num = 40  # total sampling layers
# scale = 19
# entry = 1


#####################################
# cellIDs
# cellIDs = readRootFileCellIDs(file_to_dispaly)
# # layers,chips, memo_ids, channels shape (num(events), x)
# layers, chips, memo_ids, channels = decodeCellIDs(cellIDs)
# assert entry < len(layers)
#####################################

def main():
    gui = Window()
    gui.root.mainloop()
    return None


class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CEPC ScW-ECAL + AHCAL Prototype")
        self.root.geometry('1200x800')
        # self.root.eval('tk::PlaceWindow . center')
        self.interval = 100000

        # ECAL Part
        self.ECAL_x_trans=-105
        self.ECAL_y_trans = - 19.9 * 16 # beam direction
        self.ECAL_z_trans = -105
        self.layers_num = 16
        self.Y_interval1 = 19.9
        self.Y_interval2=11.2
        self.x1_interval=5
        self.x2_interval=42
        self.number = 0
        y_ticks=[]
        for i in range(32):
            if i % 2 == 0:
                _y= (1 + i // 2 * 19.9 + self.ECAL_y_trans)
            else:
                _y = (12.2 + (i - 1) // 2 * 19.9 + self.ECAL_y_trans)
            y_ticks.append(_y)
        _y_ticks = np.array(y_ticks)
        self._y_ticks = np.concatenate([_y_ticks[::8],np.array([_y_ticks[-1]])])
        self.y_ticks = np.concatenate([np.arange(1,33,8),np.array([32])])
        self._x_ticks=np.arange(0+self.ECAL_x_trans, self.x2_interval*6+self.ECAL_x_trans, self.x2_interval)
        self.x_ticks = np.arange(105,-106,-42)
        self.z_ticks = np.arange(-105, 106, 42)
        # Prepare data.
        XE = np.arange(0, self.x1_interval * 43, self.x1_interval)
        ZE = np.arange(0, self.x2_interval * 6, self.x2_interval)
        self.XE, self.ZE = np.meshgrid(XE, ZE)
        self.unitE = np.ones((6, 43))

        ZO = np.arange(0, self.x1_interval * 43, self.x1_interval)
        XO = np.arange(0, self.x2_interval * 6, self.x2_interval)
        self.XO, self.ZO = np.meshgrid(XO, ZO)
        self.unitO = np.ones((43, 6))

        # AHCAL Part
        self.scale = 19 # num of cell border
        self.AHCAL_x_interval=40
        self.AHCAL_scale_factor=40
        self.AHCAL_x_trans = -10
        self.AHCAL_y_trans = 230  # beam direction
        self.AHCAL_z_trans = -10
        self.layers_num2 = 40
        self.number2 = 0
        y_ticks2 = np.arange(1, self.layers_num2 - 1, 5)
        self.y_ticks2 = np.concatenate([y_ticks2, np.array([self.layers_num2])])
        self._z_ticks2 = (np.array([1, 5.5, 10, 14.5, 19])+self.AHCAL_x_trans)*self.AHCAL_scale_factor
        self._x_ticks2 = self._z_ticks2[::-1]
        # Prepare data.
        X = np.arange(1+self.AHCAL_x_trans, self.scale + 1+self.AHCAL_x_trans, self.scale - 1)*self.AHCAL_scale_factor
        Z = np.arange(1+self.AHCAL_z_trans, self.scale + 1+self.AHCAL_z_trans, self.scale - 1)*self.AHCAL_scale_factor
        self.X2, self.Z2 = np.meshgrid(X, Z)
        self.unit = np.ones(self.X2.shape)


        self.p_type = ''
        self.p_energy = ''
        self.particle_information = ''

        # Frame
        self.fram_panel = tk.Frame(self.root, height=200, width=700)
        self.fram_panel.place(x=600, y=0, anchor='n')

        self.fram_deposit = tk.Frame(self.root, height=500, width=600)
        self.fram_deposit.place(x=150, y=200, anchor='nw')

        self.fram_deposit2 = tk.Frame(self.root, height=250, width=300)
        self.fram_deposit2.place(x=1050, y=200, anchor='ne')

        self.fram_deposit3 = tk.Frame(self.root, height=251, width=300)
        self.fram_deposit3.place(x=1050, y=449, anchor='ne')

        # Logo
        self.logo_file = tk.PhotoImage(file='./images.png')
        self.calice_file = tk.PhotoImage(file='./CALICELogo.png')
        # self.school_file = tk.PhotoImage(file='school.png')



        # X_DIF=np.array([7,12])
        # Z_DIF = np.array([19,24])
        # self.X_DIF,self.Z_DIF=np.meshgrid(X_DIF,Z_DIF)

        trans=350
        # dir_to_display
        tk.Label(self.fram_panel, text='ECAL:', font=('Arial', 11), width=10, height=1)\
            .place(x=105, y=0,anchor='n')
        tk.Label(self.fram_panel, text='AHCAL:', font=('Arial', 11), width=10, height=1) \
            .place(x=405, y=0, anchor='n')
        self.dir_entry = tk.Entry(self.fram_panel, width=25)
        self.dir_entry.place(x=250, y=0, anchor='n')
        self.dir2_entry = tk.Entry(self.fram_panel, width=25)
        self.dir2_entry.place(x=550, y=0, anchor='n')

        # num of events
        self.var_index_total = tk.StringVar()
        self.var_index_total.set('0/0')
        self.var_index_total2 = tk.StringVar()
        self.var_index_total2.set('0/0')
        tk.Label(self.fram_panel, textvariable=self.var_index_total).place(x=175, y=200, anchor='s')
        tk.Label(self.fram_panel, textvariable=self.var_index_total2).place(x=175+trans, y=200, anchor='s')

        # set time interval
        self.var_interval = tk.StringVar()
        self.var_interval.set('Freq: ' + str(self.interval))
        tk.Label(self.fram_panel, textvariable=self.var_interval).place(x=425, y=30, anchor='n')
        self.interval_entry = tk.Entry(self.fram_panel, width=8)  # entry_number start from 0
        self.interval_entry.place(x=338, y=30, anchor='n')

        # triggerID
        self.var_current_triggerID = tk.IntVar()
        tk.Label(self.fram_panel, text='ECAL TriggerID', font=('Arial', 11), width=12, height=1).place(x=175, y=90,
                                                                                         anchor='n')
        tk.Label(self.fram_panel, textvariable=self.var_current_triggerID, bg='yellow'
                 , font=('Arial', 15), width=10, height=1).place(x=175, y=110, anchor='n')
        self.var_current_triggerID2 = tk.IntVar()
        tk.Label(self.fram_panel, text='AHCAL TriggerID', font=('Arial', 11), width=12, height=1).place(x=175+trans, y=90,
                                                                                                  anchor='n')
        tk.Label(self.fram_panel, textvariable=self.var_current_triggerID2, bg='yellow'
                 , font=('Arial', 15), width=10, height=1).place(x=175+trans, y=110, anchor='n')
        # Index
        self.entry_index = tk.Entry(self.fram_panel, width=8)  # entry_number start from 0
        self.entry_index.place(x=135, y=140, anchor='nw')
        self.entry_index2 = tk.Entry(self.fram_panel, width=8)  # entry_number start from 0
        self.entry_index2.place(x=135+trans, y=140, anchor='nw')

        # Incident particle
        tk.Label(self.fram_panel, text='Particle:').place(x=210, y=65, anchor='n')
        tk.Label(self.fram_panel, text='Energy [GeV]:').place(x=350, y=65, anchor='n')

        self.entry_incident_particle_type = tk.Entry(self.fram_panel, width=5)  # entry_number start from 0
        self.entry_incident_particle_type.place(x=270, y=65, anchor='n')
        self.entry_incident_particle_energy = tk.Entry(self.fram_panel, width=8)  # entry_number start from 0
        self.entry_incident_particle_energy.place(x=440, y=65, anchor='n')

        # start button
        self.flag = tk.BooleanVar()
        button_start = tk.Checkbutton(self.fram_panel, text='Start', variable=self.flag,
                                      onvalue=True, offvalue=False, command=self.renewRootFilePerInterval)
        button_start.place(x=50, y=0, anchor='n')

        button1 = tk.Button(self.fram_panel, text="Plot", command=self.updateValues, width=5, height=1, )
        button1.place(x=350, y=140, anchor='n')

        previous_button = tk.Button(self.fram_panel, text="Previous", command=lambda: self.previous(ahcal=False), width=8)
        previous_button.place(x=75, y=200, anchor='s')

        next_button = tk.Button(self.fram_panel, text="Next", command=lambda: self.next(ahcal=False), width=8)
        next_button.place(x=275, y=200, anchor='s')

        previous_button2 = tk.Button(self.fram_panel, text="Previous", command=lambda: self.previous(ahcal=True), width=8)
        previous_button2.place(x=75+trans, y=200, anchor='s')

        next_button2 = tk.Button(self.fram_panel, text="Next", command=lambda: self.next(ahcal=True), width=8)
        next_button2.place(x=275+trans, y=200, anchor='s')

        interval_button = tk.Button(self.fram_panel, text="Renew Freq", command=self.renewInterval, width=6)
        interval_button.place(x=250, y=30, anchor='n')

    def updateValues(self, event=None):
        ''' ECAL use number to choose triggerID '''
        if self.entry_index.get() == '':
            self.number = 0
        else:
            self.number = int(self.entry_index.get()) - 1
        self.entry = self.picked_triggerIDs[self.number]
        self.triggerID = self.triggerIDs[self.entry]
        self.var_current_triggerID.set(self.triggerID)
        self.var_index_total.set(str(self.number + 1) + '/' + str(self.total_numbers))

        # AHCAL use number to choose triggerID
        if self.entry_index2.get() == '':
            self.number2 = 0
        else:
            self.number2 = int(self.entry_index2.get()) - 1
        self.entry2 = self.picked_triggerIDs2[self.number2]
        self.triggerID2 = self.triggerIDs2[self.entry2]
        self.var_current_triggerID2.set(self.triggerID2)
        self.var_index_total2.set(str(self.number2 + 1) + '/' + str(self.total_numbers2))

        self.p_type = self.entry_incident_particle_type.get()
        self.p_energy = self.entry_incident_particle_energy.get()
        if (self.p_type != '') and (self.p_energy != ''):
            self.particle_information = (self.p_type + '@' + self.p_energy + 'GeV')
        elif (self.p_type != '') and (self.p_energy == ''):
            self.particle_information = (self.p_type)
        elif (self.p_type == '') and (self.p_energy != ''):
            self.particle_information = ('@' + self.p_energy + 'GeV')

        # main projection
        self.plotHit(figsize=(6, 5), dpi=135, pj1=30, pj2=-40, x=300, y=255, x_ticks=self._x_ticks2,
                     y_ticks=self.y_ticks, z_ticks=self._z_ticks2, frame=self.fram_deposit,
                     xlabel_size=10, ylabel_size=10, zlabel_size=10,
                     logo=True, waterprint=True, x_label=True, y_label=True, z_label=True)
        # xy projection
        self.plotHit(figsize=(3, 2), dpi=165, pj1=0, pj2=-90, x=125, y=125, x_ticks=[''], y_ticks=[],
                     xlabel_size=5, ylabel_size=5, zlabel_size=5, projection='XY Projection',
                     z_ticks=[], tick_size=5, frame=self.fram_deposit2, z_label=False, padding=False
                     )
        # yz projection
        self.plotHit(figsize=(3, 2), dpi=180, pj1=10, pj2=6, x=120, y=125, x_ticks=[], y_ticks=(['YZ Plane']),
                     xlabel_size=5, ylabel_size=5, zlabel_size=5, projection='YZ Projection',
                     z_ticks=[], tick_size=5, frame=self.fram_deposit3, y_label=False, z_label=False)

    def loadData(self):

        self.file_to_display = self.dir_entry.get() # ECAL
        self.file_to_display2 = self.dir2_entry.get()  # AHCAL
        try:
            # ECAL
            self.file_created_time = self.file_to_display[-6:-21:-1][::-1]
            self.file_created_time = self.file_created_time[:4] + '.' + self.file_created_time[4:6] + '.' \
                                     + self.file_created_time[6:8] \
                                     + ' - ' + self.file_created_time[9:11] \
                                     + ':' + self.file_created_time[11:13] + ':' + self.file_created_time[13:15]
            # AHCAL
            self.file_created_time2 = self.file_to_display2[-6:-21:-1][::-1]
            self.file_created_time2 = self.file_created_time2[:4] + '.' + self.file_created_time2[4:6] + '.' \
                                     + self.file_created_time2[6:8] \
                                     + ' - ' + self.file_created_time2[9:11] \
                                     + ':' + self.file_created_time2[11:13] + ':' + self.file_created_time2[13:15]
        except:
            self.file_created_time = 'Time Not Known'
        # finally:
        # self.var_datatime.set(self.file_created_time)

        # ECAL cellIDs
        self.cellIDs = readRootFileCellIDs(self.file_to_display)
        # ECAL times
        self.times = readRootFileTimes(self.file_to_display)
        # ECAL hitTags
        self.tags=readRootFileHitTags(self.file_to_display)
        # layers,chips, memo_ids, channels shape (num(events), x)
        self.layers, self.chips, self.memo_ids, self.channels = decodeCellIDs(self.cellIDs)
        # ECAL triggerIDs
        self.triggerIDs = getTriggerID(self.file_to_display)
        self.picked_triggerIDs = pickTriggerIDEntry(self.triggerIDs)
        self.number = 0
        self.total_numbers = len(self.picked_triggerIDs)
        assert self.total_numbers > 0
        self.var_index_total.set(str(self.number + 1) + '/' + str(self.total_numbers))
        # ECAL current entry & triggerID
        self.entry = self.picked_triggerIDs[self.number]
        self.triggerID = self.triggerIDs[self.entry]
        self.var_current_triggerID.set(self.triggerID)

        # AHCAL cellIDs
        self.cellIDs2 = readRootFileCellIDs(self.file_to_display2)
        # ECAL times
        self.times2 = readRootFileTimes(self.file_to_display2)
        # AHCAL hitTags
        self.tags2 = readRootFileHitTags(self.file_to_display2)
        # AHCAL layers,chips, memo_ids, channels shape (num(events), x)
        self.layers2, self.chips2, self.memo_ids2, self.channels2 = decodeCellIDs(self.cellIDs2,)
        # AHCAL triggerIDs
        self.triggerIDs2 = getTriggerID(self.file_to_display2)
        self.picked_triggerIDs2 = pickTriggerIDEntry(self.triggerIDs2)
        self.number2 = 0
        self.total_numbers2 = len(self.picked_triggerIDs2)
        assert self.total_numbers2 > 0
        self.var_index_total2.set(str(self.number2 + 1) + '/' + str(self.total_numbers2))
        # AHCAL current entry & triggerID
        self.entry2 = self.picked_triggerIDs2[self.number2]
        self.triggerID2 = self.triggerIDs2[self.entry2]
        self.var_current_triggerID2.set(self.triggerID2)

    def renewRootFilePerInterval(self):

        if self.flag.get():
            self.dir = self.dir_entry.get()
            self.loadData()

            self.p_type = self.entry_incident_particle_type.get()
            self.p_energy = self.entry_incident_particle_energy.get()
            if (self.p_type != '') and (self.p_energy != ''):
                self.particle_information = (self.p_type + '@' + self.p_energy + 'GeV')
            elif (self.p_type != '') and (self.p_energy == ''):
                self.particle_information = (self.p_type)
            elif (self.p_type == '') and (self.p_energy != ''):
                self.particle_information = ('@' + self.p_energy + 'GeV')

            # Current file
            # ECAL
            self.var_current_file = tk.StringVar()
            # self.var_current_file.set('fr')
            self.var_current_file.set(self.file_to_display)
            tk.Label(self.root, textvariable=self.var_current_file).place(x=600, y=750, anchor='s')
            # AHCAL
            self.var_current_file2 = tk.StringVar()
            # self.var_current_file.set('fr')
            self.var_current_file2.set(self.file_to_display2)
            tk.Label(self.root, textvariable=self.var_current_file2).place(x=600, y=780, anchor='s')

            # TODO for test
            # main projection
            self.plotHit(figsize=(6, 5), dpi=135, pj1=30, pj2=-40, x=300, y=255, x_ticks=self._x_ticks2,
                         y_ticks=self.y_ticks, z_ticks=self._z_ticks2, frame=self.fram_deposit,
                         xlabel_size=10, ylabel_size=10, zlabel_size=10,
                         logo=True, waterprint=True, x_label=True, y_label=True, z_label=True)
            # xy projection
            self.plotHit(figsize=(3, 2), dpi=165, pj1=0, pj2=-90, x=125, y=125, x_ticks=[''], y_ticks=[],
                         xlabel_size=5, ylabel_size=5, zlabel_size=5, projection='XY Projection',
                         z_ticks=[], tick_size=5, frame=self.fram_deposit2, z_label=False, padding=False
                         )
            # yz projection
            self.plotHit(figsize=(3, 2), dpi=180, pj1=10, pj2=6, x=120, y=125, x_ticks=[], y_ticks=(['YZ Plane']),
                         xlabel_size=5, ylabel_size=5, zlabel_size=5, projection='YZ Projection',
                         z_ticks=[], tick_size=5, frame=self.fram_deposit3, y_label=False, z_label=False)
            # # tk.Label(self.fram_deposit2,text='XY Projection').place(x=0,y=0)
            # self._job = self.root.after(self.interval * 1000, self.renewRootFilePerInterval)
        else:
            # if self._job is not None:
            #     self.root.after_cancel(self._job)
            #     self._job = None
            pass
        # else:
        #     passx
        # time.sleep(self.interval)

    def renewInterval(self):
        self.interval = int(self.interval_entry.get())
        self.var_interval.set('Freq: ' + str(self.interval))

    def previous(self,ahcal=True):
        if not ahcal:
            if self.number > 0:
                self.number -= 1
                self.entry = self.picked_triggerIDs[self.number]
                self.triggerID = self.triggerIDs[self.entry]
                self.var_current_triggerID.set(self.triggerID)
                self.var_index_total.set(str(self.number + 1) + '/' + str(self.total_numbers))
            else:
                return
        else:
            if self.number2 > 0:
                self.number2 -= 1
                self.entry2 = self.picked_triggerIDs2[self.number2]
                self.triggerID2 = self.triggerIDs2[self.entry2]
                self.var_current_triggerID2.set(self.triggerID2)
                self.var_index_total2.set(str(self.number2 + 1) + '/' + str(self.total_numbers2))
            else:
                return
        # if (not ahcal and self.number > 0) or (ahcal and self.number2 < 0):
        # main projection
        self.plotHit(figsize=(6, 5), dpi=135, pj1=30, pj2=-40, x=300, y=255, x_ticks=self._x_ticks2,
                     y_ticks=self.y_ticks, z_ticks=self._z_ticks2, frame=self.fram_deposit,
                     xlabel_size=10, ylabel_size=10, zlabel_size=10,
                     logo=True, waterprint=True, x_label=True, y_label=True, z_label=True)
        # xy projection
        self.plotHit(figsize=(3, 2), dpi=165, pj1=0, pj2=-90, x=125, y=125, x_ticks=[''], y_ticks=[],
                     xlabel_size=5, ylabel_size=5, zlabel_size=5, projection='XY Projection',
                     z_ticks=[], tick_size=5, frame=self.fram_deposit2, z_label=False, padding=False
                     )
        # yz projection
        self.plotHit(figsize=(3, 2), dpi=180, pj1=10, pj2=6, x=120, y=125, x_ticks=[], y_ticks=(['YZ Plane']),
                     xlabel_size=5, ylabel_size=5, zlabel_size=5, projection='YZ Projection',
                     z_ticks=[], tick_size=5, frame=self.fram_deposit3, y_label=False, z_label=False)




    def next(self,ahcal=True):
        if not ahcal:
            if self.number < (self.total_numbers - 1):
                self.number += 1
                self.entry = self.picked_triggerIDs[self.number]
                self.triggerID = self.triggerIDs[self.entry]
                self.var_current_triggerID.set(self.triggerID)
                self.var_index_total.set(str(self.number + 1) + '/' + str(self.total_numbers))
            else:
                return
        else:
            if self.number2 < (self.total_numbers2 - 1):
                self.number2 += 1
                self.entry2 = self.picked_triggerIDs2[self.number2]
                self.triggerID2 = self.triggerIDs2[self.entry2]
                self.var_current_triggerID2.set(self.triggerID2)
                self.var_index_total2.set(str(self.number2 + 1) + '/' + str(self.total_numbers2))
            else:
                return

        # main projection
        self.plotHit(figsize=(6, 5), dpi=135, pj1=30, pj2=-40, x=300, y=255, x_ticks=self._x_ticks2,
                     y_ticks=self.y_ticks, z_ticks=self._z_ticks2, frame=self.fram_deposit,
                     xlabel_size=10, ylabel_size=10, zlabel_size=10,
                     logo=True, waterprint=True, x_label=True, y_label=True, z_label=True)
        # xy projection
        self.plotHit(figsize=(3, 2), dpi=165, pj1=0, pj2=-90, x=125, y=125, x_ticks=[''], y_ticks=[],
                     xlabel_size=5, ylabel_size=5, zlabel_size=5, projection='XY Projection',
                     z_ticks=[], tick_size=5, frame=self.fram_deposit2, z_label=False, padding=False
                     )
        # yz projection
        self.plotHit(figsize=(3, 2), dpi=180, pj1=10, pj2=6, x=120, y=125, x_ticks=[], y_ticks=(['YZ Plane']),
                     xlabel_size=5, ylabel_size=5, zlabel_size=5, projection='YZ Projection',
                     z_ticks=[], tick_size=5, frame=self.fram_deposit3, y_label=False, z_label=False)

    def ahcal_cell(self,x,y,z):
        lh1=np.array([x-20,x+20])
        lh2=np.array([y-1.5,y+1.5])
        lh3=np.array([z-20,z+20])
        hf_xy, hf_xz = np.meshgrid(lh2, lh3)  # AHCAL Face
        hf_yx, hf_yz = np.meshgrid(lh1, lh3)
        hf_zx, hf_zy = np.meshgrid(lh1, lh2)
        frame_unit = np.ones(hf_xy.shape)

    def plotHit(self, figsize, dpi, pj1, pj2, x, y, x_ticks, y_ticks, z_ticks, frame,
                tick_size=7, xlabel_size=7, ylabel_size=7, zlabel_size=7, projection=None,
                logo=False, waterprint=False, x_label=False, y_label=False, z_label=False, sub_plot=False,
                padding=True):
        '''
        1. x_ticks, y_ticks, z_tick related to the ax.set_{}ticks, not about the axis in fig.
        2. y_ticks = z axis '''

        fig = plt.figure(figsize=figsize, dpi=dpi)
        ax = fig.gca(projection='3d')
        plt.gca().set_box_aspect((1, 2, 1))
        # max times: uesd for color display
        max_times1 = np.max(self.times[self.entry])
        max_times2 = np.max(self.times2[self.entry2])
        max_times=max(max_times1,max_times2)
        alpha_frame=0.1
        # ECAL part
        # Plot the surface.
        # for i in range(32):
        #     # EBU
        #     if i%2==0:
        #         Y = self.unitE * (1+i//2*19.9+self.ECAL_y_trans)
        #         surf = ax.plot_surface(self.XE, Y, self.ZE, alpha=0.02, linewidth=0.1, antialiased=False, rstride=1,
        #                                cstride=1,
        #                                color='0.8')
        #     else:
        #         Y = self.unitO *(12.2+(i-1)//2*19.9+self.ECAL_y_trans)
        #         surf = ax.plot_surface(self.XO, Y, self.ZO, alpha=0.02, linewidth=0.1, antialiased=False, rstride=1,
        #                            cstride=1,
        #                            color='0.8')
            # DIF
            # Y_DIF=np.ones(self.X_DIF.shape)*i
            # surf_DIF = ax.plot_surface(self.X_DIF, Y_DIF, self.Z_DIF, alpha=0.3, linewidth=0.1, antialiased=False
            #                            , rstride=1, cstride=1,color='blue')
        ecal_padding=50
        # line for ECAL Frame
        # pe1=(self.ECAL_x_trans-ecal_padding,1+self.ECAL_y_trans-ecal_padding,
        #      self.x1_interval * 42+self.ECAL_x_trans-ecal_padding)
        le1=np.array([self.ECAL_x_trans-ecal_padding,self.x1_interval * 42+self.ECAL_x_trans+ecal_padding]) # x,z axis
        le2=np.array([1+self.ECAL_y_trans-ecal_padding,310.7+ self.ECAL_y_trans]) # y-axis
        ef_xy,ef_xz=np.meshgrid(le2,le1) # ECAL Face
        ef_yx,ef_yz=np.meshgrid(le1,le1)
        ef_zx,ef_zy=np.meshgrid(le1,le2)
        frame_unit=np.ones(ef_xy.shape)
        surf_xz0 = ax.plot_surface(ef_yx, le2[0]*frame_unit, ef_yz, alpha=alpha_frame, linewidth=0.1, antialiased=False, rstride=1,
                                   cstride=1,
                                   color='0.8')
        surf_xz1 = ax.plot_surface(ef_yx, le2[1] * frame_unit, ef_yz, alpha=alpha_frame, linewidth=0.1,
                                   antialiased=False, rstride=1,
                                   cstride=1,
                                   color='0.8')
        surf_xy0 = ax.plot_surface(ef_zx, ef_zy, le1[0]*frame_unit, alpha=alpha_frame, linewidth=0.1,
                                   antialiased=False, rstride=1,
                                   cstride=1,
                                   color='0.8')
        surf_xy1 = ax.plot_surface(ef_zx, ef_zy, le1[1] * frame_unit, alpha=alpha_frame, linewidth=0.1,
                                   antialiased=False, rstride=1,
                                   cstride=1,
                                   color='0.8')
        surf_yz0 = ax.plot_surface(le1[0] * frame_unit, ef_xy, ef_xz, alpha=alpha_frame, linewidth=0.1,
                                   antialiased=False, rstride=1,
                                   cstride=1,
                                   color='0.8')
        surf_yz1 = ax.plot_surface(le1[1] * frame_unit, ef_xy, ef_xz, alpha=alpha_frame, linewidth=0.1,
                                   antialiased=False, rstride=1,
                                   cstride=1,
                                   color='0.8')
        assert len(self.layers[self.entry]) == len(self.chips[self.entry])
        assert len(self.layers[self.entry]) == len(self.channels[self.entry])
        assert len(self.layers[self.entry]) == len(self.times[self.entry])


        # get positions
        x_positions, y_positions = getECALPosition(self.layers[self.entry],self.chips[self.entry],
                                                   self.channels[self.entry],self.tags[self.entry])

        for i in range(len(x_positions)):
            # plot hit
            layer_index=self.layers[self.entry][i]
            x_index = x_positions[i]
            z_index = y_positions[i]
            if x_index<0 or z_index<0 :
                continue

            if layer_index%2==0:

                x2 = np.arange(x_index*self.x1_interval+self.ECAL_x_trans, (x_index+2)*self.x1_interval+self.ECAL_x_trans, self.x1_interval)
                z2 = np.arange(z_index*self.x2_interval+self.ECAL_z_trans, (z_index+2)*self.x2_interval+self.ECAL_z_trans, self.x2_interval)
                x2, z2 = np.meshgrid(x2, z2)
                y2 = np.ones((2,2)) * (1+layer_index//2*19.9+self.ECAL_y_trans)
                surf2 = ax.plot_surface(x2, y2, z2, alpha=0.8, linewidth=0.1,
                                        antialiased=False, rstride=1, cstride=1,
                                        color=((1 - self.times[self.entry][i] / max_times) ** 2
                                               , (1 - self.times[self.entry][i] / max_times) ** 2
                                               , 1))
            else:

                x2 = np.arange(x_index * self.x2_interval+self.ECAL_x_trans, (x_index + 2) * self.x2_interval+self.ECAL_x_trans, self.x2_interval)
                z2 = np.arange(z_index * self.x1_interval+self.ECAL_z_trans, (z_index + 2) * self.x1_interval+self.ECAL_z_trans, self.x1_interval)
                x2, z2 = np.meshgrid(x2, z2)
                y2 = np.ones((2,2)) * (12.2+(layer_index-1)//2*19.9+self.ECAL_y_trans)
                surf2 = ax.plot_surface(x2, y2, z2, alpha=0.8, linewidth=0.1,
                                        antialiased=False, rstride=1, cstride=1,
                                        color=((1 - self.times[self.entry][i] / max_times) ** 2
                                               , (1 - self.times[self.entry][i] / max_times) ** 2
                                               , 1))

        # AHCAL Part
        # Plot the surface.
        # for i in range(1, self.layers_num + 1):
        #     # HBU
        #     Y2 = self.unit * i * 30.1+self.AHCAL_y_trans
        #     surf = ax.plot_surface(self.X2, Y2, self.Z2, alpha=0.02, linewidth=0.1, antialiased=False, rstride=1,
        #                            cstride=1,
        #                            color='0.8')
        ahcal_padding=100
        lh1=np.array([self.AHCAL_scale_factor*(1+self.AHCAL_x_trans)-ahcal_padding,
                      self.AHCAL_scale_factor*(self.scale +self.AHCAL_x_trans)+ahcal_padding]) # x, z
        lh2=np.array([self.AHCAL_y_trans,40*30.1+self.AHCAL_y_trans])
        hf_xy, hf_xz = np.meshgrid(lh2, lh1)  # AHCAL Face
        hf_yx, hf_yz = np.meshgrid(lh1, lh1)
        hf_zx, hf_zy = np.meshgrid(lh1, lh2)
        frame_unit = np.ones(hf_xy.shape)
        surf_xz0 = ax.plot_surface(hf_yx, lh2[0] * frame_unit, hf_yz, alpha=alpha_frame, linewidth=0.1,
                                   antialiased=False, rstride=1,
                                   cstride=1,
                                   color='0.8')
        surf_xz1 = ax.plot_surface(hf_yx, lh2[1] * frame_unit, hf_yz, alpha=alpha_frame, linewidth=0.1,
                                   antialiased=False, rstride=1,
                                   cstride=1,
                                   color='0.8')
        surf_xy0 = ax.plot_surface(hf_zx, hf_zy, lh1[0] * frame_unit, alpha=alpha_frame, linewidth=0.1,
                                   antialiased=False, rstride=1,
                                   cstride=1,
                                   color='0.8')
        surf_xy1 = ax.plot_surface(hf_zx, hf_zy, lh1[1] * frame_unit, alpha=alpha_frame, linewidth=0.1,
                                   antialiased=False, rstride=1,
                                   cstride=1,
                                   color='0.8')
        surf_yz0 = ax.plot_surface(lh1[0] * frame_unit, hf_xy, hf_xz, alpha=alpha_frame, linewidth=0.1,
                                   antialiased=False, rstride=1,
                                   cstride=1,
                                   color='0.8')
        surf_yz1 = ax.plot_surface(lh1[1] * frame_unit, hf_xy, hf_xz, alpha=alpha_frame, linewidth=0.1,
                                   antialiased=False, rstride=1,
                                   cstride=1,
                                   color='0.8')
        assert len(self.layers2[self.entry2]) == len(self.chips2[self.entry2])
        assert len(self.layers2[self.entry2]) == len(self.channels2[self.entry2])
        assert len(self.layers2[self.entry2]) == len(self.times2[self.entry2])

        x_positions2, y_positions2 = getAHCALPosition(self.chips2[self.entry2], self.channels2[self.entry2],self.tags2[self.entry2])

        for i in range(len(x_positions2)):
            # plot hit

            x_index2 = x_positions2[i]
            z_index2 = y_positions2[i]

            if x_index2>-1 and z_index2>-1:
                x2_AHCAL = np.arange(x_index2+self.AHCAL_x_trans, x_index2+self.AHCAL_x_trans + 2)*self.AHCAL_scale_factor
                z2_AHCAL = np.arange(z_index2+self.AHCAL_z_trans, z_index2+self.AHCAL_z_trans+ 2)*self.AHCAL_scale_factor
                x2_AHCAL, z2_AHCAL = np.meshgrid(x2_AHCAL, z2_AHCAL)
                y2_AHCAL = np.ones(x2_AHCAL.shape) * (1 + self.layers2[self.entry2][i])*30.1+self.AHCAL_y_trans

                surf2 = ax.plot_surface(x2_AHCAL, y2_AHCAL, z2_AHCAL, alpha=0.8, linewidth=0.1,
                                        antialiased=False, rstride=1, cstride=1,
                                        color=((1 - self.times2[self.entry2][i] / max_times) ** 2
                                               , (1 - self.times2[self.entry2][i] / max_times) ** 2
                                               , 1))


        # print mark
        if waterprint:

            plt.title('CEPC ScW-ECAL + AHCAL Prototype', fontsize=12)
            if (self.p_type == '') and (self.p_energy == ''):
                plt.suptitle('CERN SPS H8 Beamline', x=0.51, y=0.86, fontsize=10, color='grey')
            else:
                plt.suptitle('CERN SPS H8 Beamline' + '\n' + self.particle_information, x=0.51, y=0.86,
                             fontsize=10, color='grey')

        if sub_plot:
            # for good look
            sub_fontsize = 6 if dpi == 100 else 5
            plt.suptitle(projection, x=0.5, y=0.8, fontsize=sub_fontsize, color='grey')

        if frame==self.fram_deposit:
            # text: ECAL & AHCAL
            ax.text(self.ECAL_x_trans-ecal_padding-50, -400, self.x1_interval * 42+self.ECAL_x_trans+ecal_padding+50
                    ,"ScW-ECAL",'y', color='Black')
            ax.text(self.AHCAL_scale_factor*(1+self.AHCAL_x_trans)-ahcal_padding-50, 750,
                    self.AHCAL_scale_factor*(self.scale +self.AHCAL_x_trans)+ahcal_padding+50, "AHCAL",'y', color='Black')
        # # axis label
        if len(y_ticks) > 1:
            pass
        elif len(y_ticks) ==0 :
            ax.set_yticks(y_ticks)
        else:
            ax.set_yticks([500], y_ticks)

        if len(x_ticks) > 0:
            if dpi > 120:  # a little trick for good look
                ax.set_xticks([10], ['XY Plane'])
            else:
                ax.set_xticks(x_ticks, [-36, -18, 0, 18, 36])
        else:
            ax.set_xticks(x_ticks)
        if len(z_ticks) > 0:
            ax.set_zticks(z_ticks, [-36, -18, 0, 18, 36])
        else:
            ax.set_zticks(z_ticks)

        # ax.set_xticks([10], ['X'])
        # ax.set_zticks([10], ['Y'])
        ax.tick_params(labelsize=tick_size)
        if x_label:
            ax.set_xlabel('X [cm]', fontsize=xlabel_size)
        if y_label:
            ax.set_ylabel('Z [mm]', fontsize=ylabel_size)
        if z_label:
            ax.set_zlabel('Y [cm]', fontsize=zlabel_size)


        # rotate the axes and update
        # ideal direction: (30, -40)
        # test direction (0, -90)
        ax.view_init(pj1, pj2)

        # remove the background meshgrid
        ax.grid(False)

        # remove padding
        if not padding:
            plt.gca().set_position((0, 0, 1, 1))

        chart = FigureCanvasTkAgg(fig, frame)
        chart.get_tk_widget().place(x=x, y=y, anchor='center')
        if logo:
            # if (self.p_type == '') and (self.p_energy == ''):
            #     logo_fram1 = tk.Frame(frame, height=65, width=112,bg='white')
            # else:
            #     logo_fram1 = tk.Frame(frame, height=100, width=112,bg='white')
            #     tk.Label(logo_fram1, textvariable=self.var_particle_information,bg='white',font=("Arial", 13))\
            #         .place(x=56, y=100, anchor='s')
            #35 485
            logo_fram1 = tk.Frame(frame, height=65, width=112, bg='white')
            logo_fram1.place(x=35, y=13, anchor='nw')
            logo_canvas1 = tk.Canvas(logo_fram1, height=65, width=112, bg='white')
            logo_canvas1.place(x=56, y=32, anchor='center')
            logo1 = logo_canvas1.create_image(56, 0, anchor='n', image=self.logo_file)

            logo_fram2 = tk.Frame(frame, height=65, width=132, bg='white')
            logo_fram2.place(x=485, y=15, anchor='nw')
            logo_canvas2 = tk.Canvas(logo_fram2, height=65, width=132, bg='white')
            logo_canvas2.place(x=66, y=32, anchor='center')
            logo2 = logo_canvas2.create_image(60, 10, anchor='n', image=self.calice_file)

            # logo_fram2 = tk.Frame(frame, height=65, width=132, bg='blue')
            # logo_fram2.place(x=485, y=15, anchor='nw')
            tk.Label(frame,text=self.file_created_time,bg='white',fg='grey').place(x=450,y=500,anchor='s')


if __name__ == '__main__':
    main()
