import numpy as np

def rotateNormal(vector, angle_x, angle_y, angle_z):
    a = np.pi/180 * angle_x
    b = np.pi/180 * angle_y
    c = np.pi/180 * angle_z
    rotation_matrix = np.array([[np.cos(b)*np.cos(c), np.sin(a)*np.sin(b)*np.cos(c)-np.cos(a)*np.sin(c), np.cos(a)*np.sin(b)*np.cos(c)+np.sin(a)*np.sin(c)],
                            [np.cos(b)*np.sin(c), np.sin(a)*np.sin(b)*np.sin(c)+np.cos(a)*np.cos(c), np.cos(a)*np.sin(b)*np.sin(c)-np.sin(a)*np.cos(c)],
                            [-np.sin(b), np.sin(a)*np.cos(b), np.cos(a)*np.cos(b)]])
    return np.dot(rotation_matrix, vector)

def rotateAroundAxis(vector, axis, angle):
    #vector: [ux, uy, uz]
    t = np.pi/180 * angle
    rotation_matrix = np.array([[np.cos(t) +pow(axis[2], 2)*(1-np.cos(t)), axis[0]*axis[1]*(1-np.cos(t)) - axis[2]*np.sin(t), axis[0]*axis[2]*(1-np.cos(t)) + axis[1]*np.sin(t)],
                                [axis[1]*axis[0]*(1-np.cos(t)) + axis[2]*np.sin(t), np.cos(t)+pow(axis[1], 2)*(1-np.cos(t)), axis[1]*axis[2]*(1-np.cos(t))-axis[0]*np.sin(t)],
                                [axis[2]*axis[0]*(1-np.cos(t))-axis[1]*np.sin(t), axis[2]*axis[1]*(1-np.cos(t))+axis[0]*np.sin(t), np.cos(t)+pow(axis[2], 2)*(1-np.cos(t))]])
    return np.matmul(rotation_matrix, vector)

def rotateVector(alpha, beta, gamma, v):
    R = rotateEuler(alpha, beta, gamma)
    return np.dot(R, v)

def rotateEuler(alpha, beta, gamma):
    alpha_rad = np.deg2rad(alpha)  # Convert to radians
    beta_rad = np.deg2rad(beta)
    gamma_rad = np.deg2rad(gamma)
    ca = np.cos(alpha_rad)
    sa = np.sin(alpha_rad)
    cb = np.cos(beta_rad)
    sb = np.sin(beta_rad)
    cg = np.cos(gamma_rad)
    sg = np.sin(gamma_rad)
    R_x = np.array([[1, 0, 0],
                    [0, ca, -sa],
                    [0, sa, ca]])
    R_y = np.array([[cb, 0, sb],
                    [0, 1, 0],
                    [-sb, 0, cb]])
    R_z = np.array([[cg, -sg, 0],
                    [sg, cg, 0],
                    [0, 0, 1]])
    # Apply the rotations in the "intrinsic" order: X, Y, Z
    R = np.dot(R_z, np.dot(R_y, R_x))
    return R

