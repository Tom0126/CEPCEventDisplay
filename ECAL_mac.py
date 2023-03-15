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
        self.root.title("CEPC ScW-ECAL Prototype")
        self.root.geometry('1200x800')
        # self.root.eval('tk::PlaceWindow . center')
        self.layers_num = 16
        self.scale = 19
        self.interval = 100000
        self.Y_interval1 = 19.9
        self.Y_interval2=11.2
        self.x1_interval=5
        self.x2_interval=42
        self.number = 0
        y_ticks=[]
        for i in range(32):
            if i % 2 == 0:
                _y= (1 + i // 2 * 19.9 - 19.9 * 16)

            else:
                _y = (12.2 + (i - 1) // 2 * 19.9 - 19.9 * 16)
            y_ticks.append(_y)
        _y_ticks = np.array(y_ticks)
        self._y_ticks = np.concatenate([_y_ticks[::8],np.array([_y_ticks[-1]])])
        self.y_ticks = np.concatenate([np.arange(1,33,8),np.array([32])])
        self._x_ticks=np.arange(0, self.x2_interval*6, self.x2_interval)
        self.x_ticks = np.arange(105,-106,-42)
        self.z_ticks = np.arange(-105, 106, 42)
        self.p_type = ''
        self.p_energy = ''
        self.particle_information = ''

        # Frame
        self.fram_panel = tk.Frame(self.root, height=200, width=350)
        self.fram_panel.place(x=600, y=0, anchor='n')

        self.fram_deposit = tk.Frame(self.root, height=500, width=600)
        self.fram_deposit.place(x=150, y=200, anchor='nw')

        self.fram_deposit2 = tk.Frame(self.root, height=250, width=300)
        self.fram_deposit2.place(x=1050, y=200, anchor='ne')

        self.fram_deposit3 = tk.Frame(self.root, height=250, width=300)
        self.fram_deposit3.place(x=1050, y=450, anchor='ne')

        # Logo
        self.logo_file = tk.PhotoImage(file='./images.png')
        self.calice_file = tk.PhotoImage(file='./CALICELogo.png')
        # self.school_file = tk.PhotoImage(file='school.png')

        # Prepare data.
        XE = np.arange(0, self.x1_interval*43, self.x1_interval)
        ZE = np.arange(0, self.x2_interval*6, self.x2_interval)
        self.XE, self.ZE = np.meshgrid(XE, ZE)
        self.unitE = np.ones((6,43))

        ZO = np.arange(0, self.x1_interval * 43, self.x1_interval)
        XO = np.arange(0, self.x2_interval * 6, self.x2_interval)
        self.XO, self.ZO = np.meshgrid(XO, ZO)
        self.unitO = np.ones((43, 6))

        # X_DIF=np.array([7,12])
        # Z_DIF = np.array([19,24])
        # self.X_DIF,self.Z_DIF=np.meshgrid(X_DIF,Z_DIF)

        # dir_to_display
        self.dir_entry = tk.Entry(self.fram_panel, width=25)
        self.dir_entry.place(x=200, y=0, anchor='n')

        # num of events
        self.var_index_total = tk.StringVar()
        self.var_index_total.set('0/0')
        tk.Label(self.fram_panel, textvariable=self.var_index_total).place(x=175, y=200, anchor='s')

        # set time interval
        self.var_interval = tk.StringVar()
        self.var_interval.set('Freq: ' + str(self.interval))
        tk.Label(self.fram_panel, textvariable=self.var_interval).place(x=260, y=30, anchor='n')
        self.interval_entry = tk.Entry(self.fram_panel, width=8)  # entry_number start from 0
        self.interval_entry.place(x=160, y=30, anchor='n')

        # triggerID
        self.var_current_triggerID = tk.IntVar()
        tk.Label(self.fram_panel, text='TriggerID', font=('Arial', 11), width=10, height=1).place(x=175, y=90,
                                                                                                  anchor='n')
        tk.Label(self.fram_panel, textvariable=self.var_current_triggerID, bg='yellow'
                 , font=('Arial', 15), width=10, height=1).place(x=175, y=110, anchor='n')

        # Index
        self.entry_index = tk.Entry(self.fram_panel, width=8)  # entry_number start from 0
        self.entry_index.place(x=180, y=140, anchor='nw')

        # Incident particle
        tk.Label(self.fram_panel, text='Particle:').place(x=50, y=65, anchor='n')
        tk.Label(self.fram_panel, text='Energy [GeV]:').place(x=180, y=65, anchor='n')

        self.entry_incident_particle_type = tk.Entry(self.fram_panel, width=5)  # entry_number start from 0
        self.entry_incident_particle_type.place(x=105, y=65, anchor='n')
        self.entry_incident_particle_energy = tk.Entry(self.fram_panel, width=8)  # entry_number start from 0
        self.entry_incident_particle_energy.place(x=270, y=65, anchor='n')

        # start button
        self.flag = tk.BooleanVar()
        button_start = tk.Checkbutton(self.fram_panel, text='Start', variable=self.flag,
                                      onvalue=True, offvalue=False, command=self.renewRootFilePerInterval)
        button_start.place(x=50, y=0, anchor='n')

        button1 = tk.Button(self.fram_panel, text="Plot", command=self.updateValues, width=5, height=1, )
        button1.place(x=170, y=140, anchor='ne')

        previous_button = tk.Button(self.fram_panel, text="Previous", command=self.previous, width=8)
        previous_button.place(x=75, y=200, anchor='s')

        next_button = tk.Button(self.fram_panel, text="Next", command=self.next, width=8)
        next_button.place(x=275, y=200, anchor='s')

        interval_button = tk.Button(self.fram_panel, text="Renew Freq", command=self.renewInterval, width=6)
        interval_button.place(x=65, y=30, anchor='n')

    def updateValues(self, event=None):
        '''use number to choose triggerID'''
        if self.entry_index.get() == '':
            self.number = 0
        else:
            self.number = int(self.entry_index.get()) - 1
        self.entry = self.picked_triggerIDs[self.number]
        self.triggerID = self.triggerIDs[self.entry]
        self.var_current_triggerID.set(self.triggerID)
        self.var_index_total.set(str(self.number + 1) + '/' + str(self.total_numbers))

        self.p_type = self.entry_incident_particle_type.get()
        self.p_energy = self.entry_incident_particle_energy.get()
        if (self.p_type != '') and (self.p_energy != ''):
            self.particle_information = (self.p_type + '@' + self.p_energy + 'GeV')
        elif (self.p_type != '') and (self.p_energy == ''):
            self.particle_information = (self.p_type)
        elif (self.p_type == '') and (self.p_energy != ''):
            self.particle_information = ('@' + self.p_energy + 'GeV')

        # main projection
        # main plot pj1=30, pj2=-40
        self.plotHit(figsize=(6, 5), dpi=70, pj1=30, pj2=-40, x=300, y=255, x_ticks=self.x_ticks,
                     y_ticks=self.y_ticks, z_ticks=self.z_ticks, frame=self.fram_deposit,
                     xlabel_size=10, ylabel_size=10, zlabel_size=10,
                     logo=True, waterprint=True, x_label=True, y_label=True, z_label=True)
        # xy projection
        self.plotHit(figsize=(3, 2), dpi=130, pj1=0, pj2=-90, x=125, y=125, x_ticks=[''], y_ticks=[],
                     xlabel_size=5, ylabel_size=5, zlabel_size=5, projection='XY Projection',
                     z_ticks=[], tick_size=5, frame=self.fram_deposit2, z_label=False, padding=False
                     )
        # yz projection
        self.plotHit(figsize=(3, 2), dpi=120, pj1=10, pj2=6, x=120, y=125, x_ticks=[], y_ticks=(['YZ Plane']),
                     xlabel_size=5, ylabel_size=5, zlabel_size=5, projection='YZ Projection',
                     z_ticks=[], tick_size=5, frame=self.fram_deposit3, y_label=False, z_label=False)

    def loadData(self):
        try:
            self.file_to_display = getLatestRootFile(self.dir)
        except:
            self.loadData()

        try:
            self.file_created_time = self.file_to_display[-6:-21:-1][::-1]
            self.file_created_time = self.file_created_time[:4] + '.' + self.file_created_time[4:6] + '.' \
                                     + self.file_created_time[6:8] \
                                     + ' - ' + self.file_created_time[9:11] \
                                     + ':' + self.file_created_time[11:13] + ':' + self.file_created_time[13:15]
        except:
            self.file_created_time = 'Time Not Known'
        # finally:
        # self.var_datatime.set(self.file_created_time)

        # cellIDs
        self.cellIDs = readRootFileCellIDs(self.file_to_display,ahcal=False)
        # times
        self.times = readRootFileTimes(self.file_to_display,ahcal=False)
        # hitTags
        self.tags=readRootFileHitTags(self.file_to_display,ahcal=False)
        # layers,chips, memo_ids, channels shape (num(events), x)
        self.layers, self.chips, self.memo_ids, self.channels = decodeCellIDs(self.cellIDs,ahcal=False)
        # triggerIDs
        self.triggerIDs = getTriggerID(self.file_to_display,ahcal=False)
        self.picked_triggerIDs = pickTriggerIDEntry(self.triggerIDs)
        self.number = 0
        self.total_numbers = len(self.picked_triggerIDs)
        assert self.total_numbers > 0
        self.var_index_total.set(str(self.number + 1) + '/' + str(self.total_numbers))

        # current entry & triggerID
        self.entry = self.picked_triggerIDs[self.number]
        self.triggerID = self.triggerIDs[self.entry]
        self.var_current_triggerID.set(self.triggerID)

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
            self.var_current_file = tk.StringVar()
            # self.var_current_file.set('fr')
            self.var_current_file.set(self.file_to_display)
            tk.Label(self.root, textvariable=self.var_current_file).place(x=600, y=750, anchor='s')

            # TODO for test
            # main projection
            self.plotHit(figsize=(6, 5), dpi=70, pj1=30, pj2=-40, x=300, y=255, x_ticks=self.x_ticks,
                         y_ticks=self.y_ticks, z_ticks=self.z_ticks, frame=self.fram_deposit,
                         xlabel_size=10, ylabel_size=10, zlabel_size=10,
                         logo=True, waterprint=True, x_label=True, y_label=True, z_label=True)
            # xy projection
            self.plotHit(figsize=(3, 2), dpi=130, pj1=0, pj2=-90, x=125, y=125, x_ticks=[''], y_ticks=[],
                         xlabel_size=5, ylabel_size=5, zlabel_size=5, projection='XY Projection',
                         z_ticks=[], tick_size=5, frame=self.fram_deposit2, z_label=False, padding=False
                         )
            # yz projection
            self.plotHit(figsize=(3, 2), dpi=120, pj1=10, pj2=6, x=120, y=125, x_ticks=[], y_ticks=(['YZ Plane']),
                         xlabel_size=5, ylabel_size=5, zlabel_size=5, projection='YZ Projection',
                         z_ticks=[], tick_size=5, frame=self.fram_deposit3, y_label=False, z_label=False)
            # tk.Label(self.fram_deposit2,text='XY Projection').place(x=0,y=0)
            self._job = self.root.after(self.interval * 1000, self.renewRootFilePerInterval)
        else:
            if self._job is not None:
                self.root.after_cancel(self._job)
                self._job = None
            pass
        # else:
        #     pass
        # time.sleep(self.interval)

    def renewInterval(self):
        self.interval = int(self.interval_entry.get())
        self.var_interval.set('Freq: ' + str(self.interval))

    def previous(self):
        if self.number > 0:
            self.number -= 1
            self.entry = self.picked_triggerIDs[self.number]
            self.triggerID = self.triggerIDs[self.entry]
            self.var_current_triggerID.set(self.triggerID)

            self.var_index_total.set(str(self.number + 1) + '/' + str(self.total_numbers))
            # main projection
            self.plotHit(figsize=(6, 5), dpi=70, pj1=30, pj2=-40, x=300, y=255, x_ticks=self.x_ticks,
                         y_ticks=self.y_ticks, z_ticks=self.z_ticks, frame=self.fram_deposit,
                         xlabel_size=10, ylabel_size=10, zlabel_size=10,
                         logo=True, waterprint=True, x_label=True, y_label=True, z_label=True)
            # xy projection
            self.plotHit(figsize=(3, 2), dpi=130, pj1=0, pj2=-90, x=125, y=125, x_ticks=[''], y_ticks=[],
                         xlabel_size=5, ylabel_size=5, zlabel_size=5, projection='XY Projection',
                         z_ticks=[], tick_size=5, frame=self.fram_deposit2, z_label=False, padding=False
                         )
            # yz projection
            self.plotHit(figsize=(3, 2), dpi=120, pj1=10, pj2=6, x=120, y=125, x_ticks=[], y_ticks=(['YZ Plane']),
                         xlabel_size=5, ylabel_size=5, zlabel_size=5, projection='YZ Projection',
                         z_ticks=[], tick_size=5, frame=self.fram_deposit3, y_label=False, z_label=False)
        else:
            pass

    def next(self):
        if self.number < (self.total_numbers - 1):
            self.number += 1
            self.entry = self.picked_triggerIDs[self.number]
            self.triggerID = self.triggerIDs[self.entry]
            self.var_current_triggerID.set(self.triggerID)
            self.var_index_total.set(str(self.number + 1) + '/' + str(self.total_numbers))
            # main projection
            self.plotHit(figsize=(6, 5), dpi=70, pj1=30, pj2=-40, x=300, y=255, x_ticks=self.x_ticks,
                         y_ticks=self.y_ticks, z_ticks=self.z_ticks, frame=self.fram_deposit,
                         xlabel_size=10, ylabel_size=10, zlabel_size=10,
                         logo=True, waterprint=True, x_label=True, y_label=True, z_label=True)
            # xy projection
            self.plotHit(figsize=(3, 2), dpi=130, pj1=0, pj2=-90, x=125, y=125, x_ticks=[''], y_ticks=[],
                         xlabel_size=5, ylabel_size=5, zlabel_size=5, projection='XY Projection',
                         z_ticks=[], tick_size=5, frame=self.fram_deposit2, z_label=False, padding=False
                         )
            # yz projection
            self.plotHit(figsize=(3, 2), dpi=120, pj1=10, pj2=6, x=120, y=125, x_ticks=[], y_ticks=(['YZ Plane']),
                         xlabel_size=5, ylabel_size=5, zlabel_size=5, projection='YZ Projection',
                         z_ticks=[], tick_size=5, frame=self.fram_deposit3, y_label=False, z_label=False)
        else:
            pass

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
        # Plot the surface.

        for i in range(32):
            # EBU
            if i%2==0:
                Y = self.unitE * (1+i//2*19.9-19.9*16)
                surf = ax.plot_surface(self.XE, Y, self.ZE, alpha=0.02, linewidth=0.1, antialiased=False, rstride=1,
                                       cstride=1,
                                       color='0.8')
            else:
                Y = self.unitO *(12.2+(i-1)//2*19.9-19.9*16)
                surf = ax.plot_surface(self.XO, Y, self.ZO, alpha=0.02, linewidth=0.1, antialiased=False, rstride=1,
                                   cstride=1,
                                   color='0.8')
            # DIF
            # Y_DIF=np.ones(self.X_DIF.shape)*i
            # surf_DIF = ax.plot_surface(self.X_DIF, Y_DIF, self.Z_DIF, alpha=0.3, linewidth=0.1, antialiased=False
            #                            , rstride=1, cstride=1,color='blue')

        assert len(self.layers[self.entry]) == len(self.chips[self.entry])
        assert len(self.layers[self.entry]) == len(self.channels[self.entry])
        assert len(self.layers[self.entry]) == len(self.times[self.entry])
        # max times: uesd for color display
        max_times = np.max(self.times[self.entry])

        # get positions
        x_positions, y_positions = getECALPosition(self.layers[self.entry],self.chips[self.entry],
                                                   self.channels[self.entry],self.tags[self.entry])

        for i in range(len(self.layers[self.entry])):
            # plot hit
            layer_index=self.layers[self.entry][i]
            print(layer_index)
            x_index = x_positions[i]
            z_index = y_positions[i]
            if x_index<0 or z_index<0 :
                continue
            if layer_index%2==0:
                x2 = np.arange(x_index*self.x1_interval, (x_index+2)*self.x1_interval, self.x1_interval)
                z2 = np.arange(z_index*self.x2_interval, (z_index+2)*self.x2_interval, self.x2_interval)
                x2, z2 = np.meshgrid(x2, z2)
                y2 = np.ones((2,2)) * (1+layer_index//2*19.9-19.9*16)
                surf2 = ax.plot_surface(x2, y2, z2, alpha=0.8, linewidth=0.1,
                                        antialiased=False, rstride=1, cstride=1,
                                        color=((1 - self.times[self.entry][i] / max_times) ** 2
                                               , (1 - self.times[self.entry][i] / max_times) ** 2
                                               , 1))
            else:
                x2 = np.arange(x_index * self.x2_interval, (x_index + 2) * self.x2_interval, self.x2_interval)
                z2 = np.arange(z_index * self.x1_interval, (z_index + 2) * self.x1_interval, self.x1_interval)
                x2, z2 = np.meshgrid(x2, z2)
                y2 = np.ones((2,2)) * (12.2+(layer_index-1)//2*19.9-19.9*16)
                surf2 = ax.plot_surface(x2, y2, z2, alpha=0.8, linewidth=0.1,
                                        antialiased=False, rstride=1, cstride=1,
                                        color=((1 - self.times[self.entry][i] / max_times) ** 2
                                               , (1 - self.times[self.entry][i] / max_times) ** 2
                                               , 1))


        # print mark
        if waterprint:

            plt.title('CEPC ScW-ECAL Prototype', fontsize=15)
            if (self.p_type == '') and (self.p_energy == ''):
                plt.suptitle('CERN SPS H8 Beamline', x=0.51, y=0.86, fontsize=10, color='grey')
            else:
                plt.suptitle('CERN SPS H8 Beamline' + '\n' + self.particle_information, x=0.51, y=0.86,
                             fontsize=10, color='grey')

        if sub_plot:
            # for good look
            sub_fontsize = 6 if dpi == 100 else 5
            plt.suptitle(projection, x=0.5, y=0.8, fontsize=sub_fontsize, color='grey')

        # axis label
        if len(y_ticks) != 1:
            ax.set_yticks(self._y_ticks,y_ticks)
        else:
            ax.set_yticks([-150], y_ticks)

        if len(x_ticks) > 0:
            if dpi > 120:  # a little trick for good look
                ax.set_xticks([100], ['XY Plane'])
            else:
                ax.set_xticks(self._x_ticks,x_ticks)
        else:
            ax.set_xticks(x_ticks)
        if len(z_ticks) > 0:
            ax.set_zticks(self._x_ticks,z_ticks)
        else:
            ax.set_zticks(z_ticks)

        ax.tick_params(labelsize=tick_size)
        if x_label:
            ax.set_xlabel('X [mm]', fontsize=xlabel_size)
        if y_label:
            ax.set_ylabel('Layer', fontsize=ylabel_size)
        if z_label:
            ax.set_zlabel('Y [mm]', fontsize=zlabel_size)


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
