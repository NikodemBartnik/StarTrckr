import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



def drawPlot(a, b, c):
    global vector
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlabel(r'$x$', fontsize='large')
    ax.set_ylabel(r'$y$', fontsize='large')
    ax.set_zlabel(r'$z$', fontsize='large')
    ax.quiver(0, 0, 0, 2, 0, 0, color='k', arrow_length_ratio=0.05) # x-axis
    ax.quiver(0, 0, 0, 0, 2, 0, color='k', arrow_length_ratio=0.05) # y-axis
    ax.quiver(0, 0, 0, 0, 0, 2, color='k', arrow_length_ratio=0.05) # z-axis

    ax.quiver(0,0,0, a[0], a[1], a[2])
    ax.quiver(0,0,0, b[0], b[1], b[2])
    ax.quiver(0,0,0, c[0], c[1], c[2], color='r')
    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])
    plt.show()


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

rot_axis = np.array([1, 0, 0])   
init_vector = np.array([1, 1, 0])   
rot_axis = rot_axis/np.sqrt(pow(rot_axis[0], 2) + pow(rot_axis[1], 2) + pow(rot_axis[2], 2))

print('rot_axis_vector: ', rot_axis)
print('after rotation: ', rotateNormal(rot_axis, 0, 52, 0))

print(rot_axis)
print(rotateAroundAxis(init_vector, rot_axis, 180))


drawPlot(init_vector, rotateAroundAxis(init_vector, rot_axis, 10), rot_axis)
