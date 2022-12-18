import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import animation


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_xlabel(r'$x$', fontsize='large')
ax.set_ylabel(r'$y$', fontsize='large')
ax.set_zlabel(r'$z$', fontsize='large')
ax.quiver(0, 0, 0, 2, 0, 0, color='k', arrow_length_ratio=0.05) # x-axis
ax.quiver(0, 0, 0, 0, 2, 0, color='k', arrow_length_ratio=0.05) # y-axis
ax.quiver(0, 0, 0, 0, 0, 2, color='k', arrow_length_ratio=0.05) # z-axis



def updatePlot(a):
        global final_vector_x, final_vector_z

        final_vector_x = rotateAroundAxis(final_vector_x, rot_ref_vec_x, 0)
        final_vector_z = rotateAroundAxis(final_vector_z, rot_ref_vec_x, 0)

        ax.clear()
        ax.quiver(0,0,0, rot_ref_vec_x[0], rot_ref_vec_x[1], rot_ref_vec_x[2], color='r')
        ax.quiver(0,0,0, final_vector_x[0], final_vector_x[1], final_vector_x[2], color='b')
        ax.quiver(0,0,0, final_vector_z[0], final_vector_z[1], final_vector_z[2], color='g')
    
        ax.set_xlim([-1.2, 1.2])
        ax.set_ylim([-1.2, 1.2])
        ax.set_zlim([-1.2, 1.2])
        print('XA: ', np.round(np.arccos(np.dot(final_vector_x, ref_vec_x)) * 180/np.pi, 2), 
              ' XB: ', np.round(np.arccos(np.dot(final_vector_x, ref_vec_y)) * 180/np.pi, 2),
              ' XZ: ', np.round(np.arccos(np.dot(final_vector_x, ref_vec_z)) * 180/np.pi, 2),
              ' ZA: ', np.round(np.arccos(np.dot(final_vector_z, ref_vec_x)) * 180/np.pi, 2),
              ' ZB: ', np.round(np.arccos(np.dot(final_vector_z, ref_vec_y)) * 180/np.pi, 2),
              ' ZC: ', np.round(np.arccos(np.dot(final_vector_z, ref_vec_z)) * 180/np.pi, 2))
        fig.canvas.draw()


def rotateNormal(vector, angle_x, angle_y, angle_z):
    a = np.pi/180 * angle_x
    b = np.pi/180 * angle_y
    c = np.pi/180 * angle_z
    rotation_matrix = np.array([[np.cos(b)*np.cos(c), np.sin(a)*np.sin(b)*np.cos(c), np.cos(a)*np.sin(b)*np.cos(c)+np.sin(a)*np.sin(c)],
                            [np.cos(b)*np.sin(c), np.sin(a)*np.sin(b)*np.sin(c)+np.cos(a)*np.cos(c), np.cos(a)*np.sin(b)*np.sin(c)-np.sin(a)*np.cos(c)],
                            [-np.sin(b), np.sin(a)*np.cos(b), np.cos(a)*np.cos(b)]])
    return np.matmul(rotation_matrix, vector)

def rotateAroundAxis(v, axis, angle):
    #vector: [ux, uy, uz]
    t = np.pi/180 * angle
    rotation_matrix = np.array([[np.cos(t) +pow(axis[2], 2)*(1-np.cos(t)), axis[0]*axis[1]*(1-np.cos(t)) - axis[2]*np.sin(t), axis[0]*axis[2]*(1-np.cos(t)) + axis[1]*np.sin(t)],
                                [axis[1]*axis[0]*(1-np.cos(t)) + axis[2]*np.sin(t), np.cos(t)+pow(axis[1], 2)*(1-np.cos(t)), axis[1]*axis[2]*(1-np.cos(t))-axis[0]*np.sin(t)],
                                [axis[2]*axis[0]*(1-np.cos(t))-axis[1]*np.sin(t), axis[2]*axis[1]*(1-np.cos(t))+axis[0]*np.sin(t), np.cos(t)+pow(axis[2], 2)*(1-np.cos(t))]])
    return np.matmul(rotation_matrix, v)

ref_vec_x = np.array([1, 0, 0])
ref_vec_y = np.array([0, 1, 0])
ref_vec_z = np.array([0, 0, 1])

rot_ref_vec_x = rotateNormal(ref_vec_x, 0, 0, 20)
rot_ref_vec_z = rotateNormal(ref_vec_z, 0, 0, 20)

final_vector_x = rotateNormal(rot_ref_vec_x, 0, 0, 0)
final_vector_z = rotateNormal(rot_ref_vec_z, 0, 0, 0)


ani = animation.FuncAnimation(fig, updatePlot, frames=np.arange(0, 360, 1), interval=20)
plt.show()