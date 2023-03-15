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
        self.root.title("CEPC AHCAL Prototype")
        self.root.geometry('800x800')
        self.root.eval('tk::PlaceWindow . center')
        self.layers_num = 40
        self.scale = 19
        self.interval = 5
        self.number = 0
        y_ticks = np.arange(1, self.layers_num - 1, 2)
        y_ticks = np.concatenate([y_ticks, np.array([self.layers_num])])
        self.y_ticks = y_ticks

        # CEPC logo
        self.logo_file = tk.PhotoImage(file='images.png')
        self.school_file = tk.PhotoImage(file='school.png')

        self.logo_fram1 = tk.Frame(self.root, height=65, width=111)
        self.logo_fram1.place(x=50, y=20, anchor='nw')
        self.logo_canvas1 = tk.Canvas(self.logo_fram1, height=65, width=111)
        self.logo_canvas1.pack()
        self.logo1 = self.logo_canvas1.create_image(0, 0, anchor='nw', image=self.logo_file)

        self.logo_fram2 = tk.Frame(self.root, height=112, width=174)
        self.logo_fram2.place(x=630, y=20, anchor='nw')
        self.logo_canvas2 = tk.Canvas(self.logo_fram2, height=112, width=174)
        self.logo_canvas2.pack()
        self.logo2 = self.logo_canvas2.create_image(0, 0, anchor='nw', image=self.school_file)

        # Data time
        # self.datatime_fram1 = tk.Frame(self.root, height=30, width=111)
        # self.datatime_fram1.place(x=200, y=660, anchor='nw')
        # self.var_datatime = tk.StringVar()
        # tk.Label(self.datatime_fram1, text='Time:',
        #          font=('Arial', 15), width=20, height=1).pack()
        #
        # self.datatime_fram2 = tk.Frame(self.root, height=30, width=111,bg='blue')
        # self.datatime_fram2.place(x=330, y=660, anchor='nw')
        # self.var_datatime = tk.StringVar()
        # tk.Label(self.datatime_fram2, textvariable=self.var_datatime,bg='Yellow',
        #          font=('Arial', 15), width=20, height=1).pack()

        # Prepare data.
        X = np.arange(1, self.scale + 1, 1)
        Z = np.arange(1, self.scale + 1, 1)
        self.X, self.Z = np.meshgrid(X, Z)
        self.unit = np.ones(self.X.shape)

        # X_DIF=np.array([7,12])
        # Z_DIF = np.array([19,24])
        # self.X_DIF,self.Z_DIF=np.meshgrid(X_DIF,Z_DIF)

        # dir_to_display
        self.dir_entry = tk.Entry(self.root, width=25)
        self.dir_entry.place(x=350, y=0, anchor='nw')

        # num of events
        self.var_total_numbers = tk.IntVar()
        # self.var_total_numbers.set(self.total_numbers)
        tk.Label(self.root, text='Total Numbers:').place(x=300, y=30, anchor='nw')
        tk.Label(self.root, textvariable=self.var_total_numbers).place(x=395, y=30, anchor='nw')

        # set time interval
        self.var_interval = tk.IntVar()
        self.var_interval.set(self.interval)
        tk.Label(self.root, text='Frequency:').place(x=420, y=30, anchor='nw')
        self.interval_entry = tk.Entry(self.root, width=5)  # entry_number start from 0
        self.interval_entry.place(x=490, y=30, anchor='nw')
        tk.Label(self.root, textvariable=self.var_interval).place(x=550, y=30, anchor='nw')


        # triggerID
        self.var_current_triggerID = tk.IntVar()
        tk.Label(self.root, text='TriggerID', font=('Arial', 11), width=10, height=1).place(x=370, y=90)
        tk.Label(self.root, textvariable=self.var_current_triggerID, bg='yellow'
                 , font=('Arial', 15), width=10, height=1).place(x=359, y=110, anchor='nw')
        tk.Label(self.root, text="Number:").place(x=180, y=30, anchor='nw')
        self.entry_number = tk.Entry(self.root, width=5)  # entry_number start from 0
        self.entry_number.place(x=250, y=30, anchor='nw')

        self.flag = tk.BooleanVar()
        button_start = tk.Checkbutton(self.root, text='Start', variable=self.flag,
                                      onvalue=True, offvalue=False, command=self.renewRootFilePerInterval)
        button_start.place(x=277, y=0, anchor='nw')

        button1 = tk.Button(self.root, text="Plot", command=self.updateValues, width=10, height=1,)
        button1.place(x=300, y=60, anchor='nw')

        previous_button = tk.Button(self.root, text="Previous", command=self.previous, width=8)
        previous_button.place(x=250, y=105, anchor='nw')

        next_button = tk.Button(self.root, text="Next", command=self.next, width=8)
        next_button.place(x=500, y=105, anchor='nw')

        interval_button = tk.Button(self.root, text="Renew Freq", command=self.renewInterval, width=10)
        interval_button.place(x=400, y=60, anchor='nw')

        # Frame
        self.fram_deposit = tk.Frame(self.root, height=500, width=600)
        self.fram_deposit.place(x=100, y=150, anchor='nw')

    def updateValues(self, event=None):
        '''use number to choose triggerID'''
        if self.entry_number.get() == '':
            self.number = 0
        else:
            self.number = int(self.entry_number.get())
        self.entry = self.picked_triggerIDs[self.number]
        self.triggerID = self.triggerIDs[self.entry]
        self.var_current_triggerID.set(self.triggerID)
        self.plotHit()

    def loadData(self):
        self.file_to_display = getLatestRootFile(self.dir)

        try:
            self.file_created_time = self.file_to_display[-6:-21:-1][::-1]
        except:
            self.file_created_time = 'Time Not Known'
        finally:
            self.var_datatime.set(self.file_created_time)

        # cellIDs
        self.cellIDs = readRootFileCellIDs(self.file_to_display)
        # layers,chips, memo_ids, channels shape (num(events), x)
        self.layers, self.chips, self.memo_ids, self.channels = decodeCellIDs(self.cellIDs)
        # triggerIDs
        self.triggerIDs = getTriggerID(self.file_to_display)
        self.picked_triggerIDs = pickTriggerIDEntry(self.triggerIDs)
        self.number = 0
        self.total_numbers = len(self.picked_triggerIDs)
        assert self.total_numbers > 0
        self.var_total_numbers.set(self.total_numbers)

        # current entry & triggerID
        self.entry = self.picked_triggerIDs[self.number]
        self.triggerID = self.triggerIDs[self.entry]
        self.var_current_triggerID.set(self.triggerID)

    def renewRootFilePerInterval(self):
        if self.flag.get():
            self.dir = self.dir_entry.get()
            self.loadData()
            self.plotHit()
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
        self.var_interval.set(self.interval)

    def previous(self):
        if self.number > 0:
            self.number -= 1
            self.entry = self.picked_triggerIDs[self.number]
            self.triggerID = self.triggerIDs[self.entry]
            self.var_current_triggerID.set(self.triggerID)
            self.plotHit()
        else:
            pass

    def next(self):
        if self.number < (self.total_numbers - 1):
            self.number += 1
            self.entry = self.picked_triggerIDs[self.number]
            self.triggerID = self.triggerIDs[self.entry]
            self.var_current_triggerID.set(self.triggerID)
            self.plotHit()
        else:
            pass

    def plotHit(self):
        fig = plt.figure(figsize=(6, 5), dpi=80)
        ax = fig.gca(projection='3d')
        plt.gca().set_box_aspect((1, 4, 1))
        # Plot the surface.

        for i in range(1, self.layers_num + 1):
            # HBU
            Y = self.unit * i
            surf = ax.plot_surface(self.X, Y, self.Z, alpha=0.1, linewidth=0.1, antialiased=False, rstride=1, cstride=1,
                                   color='green')
            # DIF
            # Y_DIF=np.ones(self.X_DIF.shape)*i
            # surf_DIF = ax.plot_surface(self.X_DIF, Y_DIF, self.Z_DIF, alpha=0.3, linewidth=0.1, antialiased=False
            #                            , rstride=1, cstride=1,color='blue')

        assert len(self.layers[self.entry]) == len(self.chips[self.entry])
        assert len(self.layers[self.entry]) == len(self.channels[self.entry])

        x_positions, y_positions = getPosition(self.chips[self.entry], self.channels[self.entry])

        for i in range(len(self.layers[self.entry])):
            # plot hit
            x_index = x_positions[i]
            z_index = y_positions[i]
            x2 = np.arange(x_index, x_index + 2)
            z2 = np.arange(z_index, z_index + 2)
            x2, z2 = np.meshgrid(x2, z2)
            y2 = np.ones(x2.shape) * (1 + self.layers[self.entry][i])

            surf2 = ax.plot_surface(x2, y2, z2, alpha=1 * 2 ** (-self.layers[self.entry][i] / 20), linewidth=0.1,
                                    antialiased=False, rstride=1, cstride=1, color='red')
        # print mark
        ax.set_title('CEPC AHCAL Prototype')

        # axis label
        ax.set_yticks(self.y_ticks)
        ax.set_xticks([10], ['X'])
        ax.set_zticks([10], ['Y'])
        ax.tick_params(labelsize=7)
        # ax.set_xlabel('X')
        # ax.set_zlabel('Y')
        ax.set_ylabel('Layer')

        # rotate the axes and update
        for angle in range(0, 360):
            # ideal direction: (30, -40)
            # test direction (0, -90)
            ax.view_init(30, -40)

        # remove the background meshgrid
        ax.grid(False)

        # remove padding
        plt.gca().set_position((0, 0, 1, 1))

        chart = FigureCanvasTkAgg(fig, self.fram_deposit)
        chart.get_tk_widget().place(x=300, y=250, anchor='center')


if __name__ == '__main__':
    main()
