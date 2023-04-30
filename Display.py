
from DecodePosition import *

from ReadRoot import *


# In this version, only read valid triggerIDs





class Window:
    def __init__(self, ecal_path, ahcal_path):

        self.ecal_path=ecal_path
        self.ahcal_path=ahcal_path


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






        # ECAL cellIDs
        self.cellIDs = readRootFileCellIDs(self.ecal_path)
        # ECAL times
        self.times = readRootFileTimes(self.ecal_path)
        # layers,chips, memo_ids, channels shape (num(events), x)
        self.layers, self.chips, self.memo_ids, self.channels = decodeCellIDs(self.cellIDs)
        # ECAL triggerIDs
        self.triggerIDs = getTriggerID(self.ecal_path)
        self.picked_triggerIDs = pickTriggerIDEntry(self.triggerIDs)



        # AHCAL cellIDs
        self.cellIDs2 = readRootFileCellIDs(self.ahcal_path)
        # ECAL times
        self.times2 = readRootFileTimes(self.ahcal_path)
        # AHCAL layers,chips, memo_ids, channels shape (num(events), x)
        self.layers2, _, _, _ = decodeCellIDs(self.cellIDs2, )
        self.hit_x2 = getHit_X(self.ahcal_path)
        self.hit_y2 = getHit_Y(self.ahcal_path)

        # AHCAL triggerIDs
        self.triggerIDs2 = getTriggerID(self.ahcal_path)
        self.picked_triggerIDs2 = pickTriggerIDEntry(self.triggerIDs2)


    def ahcal_cell(self,x,y,z):
        lh1=np.array([x-20,x+20])
        lh2=np.array([y-1.5,y+1.5])
        lh3=np.array([z-20,z+20])
        hf_xy, hf_xz = np.meshgrid(lh2, lh3)  # AHCAL Face
        hf_yx, hf_yz = np.meshgrid(lh1, lh3)
        hf_zx, hf_zy = np.meshgrid(lh1, lh2)
        frame_unit = np.ones(hf_xy.shape)

    def plotHit(self,ecal_entry,ahcal_entry,save_dir,):
        '''
        1. x_ticks, y_ticks, z_tick related to the ax.set_{}ticks, not about the axis in fig.
        2. y_ticks = z axis '''
        fig = plt.figure(figsize=(6, 5))
        ax = fig.add_subplot(projection='3d')
        plt.gca().set_box_aspect((1, 2, 1))

        # max times: uesd for color display
        max_times1 = np.amax(self.times[ecal_entry])
        max_times2 = np.amax(self.times2[ahcal_entry])
        max_times=max(max_times1,max_times2)
        alpha_frame=0.1

        ecal_padding=50

        # ECAL
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
        assert len(self.layers[ecal_entry]) == len(self.chips[ecal_entry])
        assert len(self.layers[ecal_entry]) == len(self.channels[ecal_entry])
        assert len(self.layers[ecal_entry]) == len(self.times[ecal_entry])


        # get positions
        x_positions, y_positions = getECALPosition(self.layers[ecal_entry],self.chips[ecal_entry],
                                                   self.channels[ecal_entry])

        for i in range(len(x_positions)):
            # plot hit
            layer_index=self.layers[ecal_entry][i]
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
                                        color=((1 - self.times[ecal_entry][i] / max_times) ** 2
                                               , (1 - self.times[ecal_entry][i] / max_times) ** 2
                                               , 1))
            else:

                x2 = np.arange(x_index * self.x2_interval+self.ECAL_x_trans, (x_index + 2) * self.x2_interval+self.ECAL_x_trans, self.x2_interval)
                z2 = np.arange(z_index * self.x1_interval+self.ECAL_z_trans, (z_index + 2) * self.x1_interval+self.ECAL_z_trans, self.x1_interval)
                x2, z2 = np.meshgrid(x2, z2)
                y2 = np.ones((2,2)) * (12.2+(layer_index-1)//2*19.9+self.ECAL_y_trans)
                surf2 = ax.plot_surface(x2, y2, z2, alpha=0.8, linewidth=0.1,
                                        antialiased=False, rstride=1, cstride=1,
                                        color=((1 - self.times[ecal_entry][i] / max_times) ** 2
                                               , (1 - self.times[ecal_entry][i] / max_times) ** 2
                                               , 1))

        # AHCAL Part
        # Plot the surface.

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
        assert len(self.layers2[ahcal_entry]) == len(self.hit_x2[ahcal_entry])
        assert len(self.layers2[ahcal_entry]) == len(self.hit_y2[ahcal_entry])
        assert len(self.layers2[ahcal_entry]) == len(self.times2[ahcal_entry])

        x_positions2, y_positions2 = getAHCALPosition(self.hit_x2[ahcal_entry], self.hit_y2[ahcal_entry])

        for i in range(len(x_positions2)):
            # plot hit

            x_index2 = x_positions2[i]
            z_index2 = y_positions2[i]

            if x_index2>-1 and z_index2>-1:
                x2_AHCAL = np.arange(x_index2+self.AHCAL_x_trans, x_index2+self.AHCAL_x_trans + 2)*self.AHCAL_scale_factor
                z2_AHCAL = np.arange(z_index2+self.AHCAL_z_trans, z_index2+self.AHCAL_z_trans+ 2)*self.AHCAL_scale_factor
                x2_AHCAL, z2_AHCAL = np.meshgrid(x2_AHCAL, z2_AHCAL)
                y2_AHCAL = np.ones(x2_AHCAL.shape) * (1 + self.layers2[ahcal_entry][i])*30.1+self.AHCAL_y_trans

                surf2 = ax.plot_surface(x2_AHCAL, y2_AHCAL, z2_AHCAL, alpha=0.8, linewidth=0.1,
                                        antialiased=False, rstride=1, cstride=1,
                                        color=((1 - self.times2[ahcal_entry][i] / max_times) ** 2
                                               , (1 - self.times2[ahcal_entry][i] / max_times) ** 2
                                               , 1))




        plt.title('CEPC ScW-ECAL + AHCAL Prototype', fontsize=12)





        # text: ECAL & AHCAL
        ax.text(self.ECAL_x_trans-ecal_padding-50, -400, self.x1_interval * 42+self.ECAL_x_trans+ecal_padding+50
                ,"ScW-ECAL",'y', color='Black')
        ax.text(self.AHCAL_scale_factor*(1+self.AHCAL_x_trans)-ahcal_padding-50, 750,
                self.AHCAL_scale_factor*(self.scale +self.AHCAL_x_trans)+ahcal_padding+50, "AHCAL",'y', color='Black')



        ax.tick_params(labelsize=7)

        ax.set_xlabel('X [cm]', fontsize=7)

        ax.set_ylabel('Z [mm]', fontsize=7)

        ax.set_zlabel('Y [cm]', fontsize=7)


        ax.view_init(30, -40)

        # remove the background meshgrid
        ax.grid(False)

        # remove padding

        plt.gca().set_position((0, 0, 1, 1))

        save_path=os.path.join(save_dir,'{}_{}.png'.format(ecal_entry,ahcal_entry))
        plt.savefig(save_path)

if __name__ == '__main__':

    ecal_path='/home/songsy/CEPCEventDisplay/data/mnt2/ScECAL/2023/Result/calib/mu-/100GeV/ECAL_Run10_20230425_003153.root'
    ahcal_path='/home/songsy/CEPCEventDisplay/data/mnt2/AHCAL/PublicAna/2023/BeamAna/result/mu-/100GeV/AHCAL_Run10_20230425_003339.root'
    ecal_entry=0
    ahcal_entry=0
    save_dir='Result' #directory
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    display=Window(ecal_path=ecal_path,ahcal_path=ahcal_path)
    display.plotHit(ecal_entry=ecal_entry,ahcal_entry=ahcal_entry,save_dir=save_dir)
    display.plotHit(ecal_entry=5, ahcal_entry=6,save_dir=save_dir)


    pass
