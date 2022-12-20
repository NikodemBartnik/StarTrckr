import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation

class PlotVisualizer:
    def __init__(self, ref_vec_x, ref_vec_z, polar_vec_x, polar_vec_z, tracker_vec_x, tracker_vec_z):
        global ani
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ref_vec_x = ref_vec_x
        self.ref_vec_z = ref_vec_z
        self.polar_vec_x = polar_vec_x
        self.polar_vec_z = polar_vec_z
        self.tracker_vec_x = tracker_vec_x
        self.tracker_vec_z = tracker_vec_z

        self.ani = animation.FuncAnimation(self.fig, self.updatePlot, frames=np.arange(0, 360, 1), interval=20)
        plt.ion()
        plt.show()

    def updateVectors(self, ref_vec_x, ref_vec_z, polar_vec_x, polar_vec_z, tracker_vec_x, tracker_vec_z):
        self.ref_vec_x = ref_vec_x
        self.ref_vec_z = ref_vec_z
        self.polar_vec_x = polar_vec_x
        self.polar_vec_z = polar_vec_z
        self.tracker_vec_x = tracker_vec_x
        self.tracker_vec_z = tracker_vec_z


    def updatePlot(self, a):
        print('update called')
        self.ax.set_xlabel(r'$x$', fontsize='large')
        self.ax.set_ylabel(r'$y$', fontsize='large')
        self.ax.set_zlabel(r'$z$', fontsize='large')
        self.ax.quiver(0, 0, 0, 2, 0, 0, color='k', arrow_length_ratio=0.05) # x-axis
        self.ax.quiver(0, 0, 0, 0, 2, 0, color='k', arrow_length_ratio=0.05) # y-axis
        self.ax.quiver(0, 0, 0, 0, 0, 2, color='k', arrow_length_ratio=0.05) # z-axis

        self.ax.clear()
        self.ax.quiver(0,0,0, self.ref_vec_x[0], self.ref_vec_x[1], self.ref_vec_x[2], color='#AC0E09')
        self.ax.quiver(0,0,0, self.ref_vec_z[0], self.ref_vec_z[1], self.ref_vec_z[2], color='#E63C36')

        self.ax.quiver(0,0,0, self.polar_vec_x[0], self.polar_vec_x[1], self.polar_vec_x[2], color='#02A232')
        self.ax.quiver(0,0,0, self.polar_vec_z[0], self.polar_vec_z[1], self.polar_vec_z[2], color='#36E66B')

        self.ax.quiver(0,0,0, self.tracker_vec_x[0], self.tracker_vec_x[1], self.tracker_vec_x[2], color='#1368B3')
        self.ax.quiver(0,0,0, self.tracker_vec_z[0], self.tracker_vec_z[1], self.tracker_vec_z[2], color='#45A4F7')
    
        self.ax.set_xlim([-1.2, 1.2])
        self.ax.set_ylim([-1.2, 1.2])
        self.ax.set_zlim([-1.2, 1.2])
        self.fig.canvas.draw()