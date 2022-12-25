import TrackerMath as tm
import numpy as np

class TrackerController:
    def __init__(self):
        self.ref_vec_x = np.array([1, 0, 0], dtype=np.longdouble)
        self.ref_vec_y = np.array([0, 1, 0], dtype=np.longdouble)
        self.ref_vec_z = np.array([0, 0, 1], dtype=np.longdouble)

        self.polar_vec_x = self.ref_vec_x
        self.polar_vec_z = self.ref_vec_z

        self.tracker_vec_x = self.ref_vec_x
        self.tracker_vec_z = self.ref_vec_z
        self.c_rotation = 0
        

    def polarAlign(self):
        self.polar_vec_x = self.tracker_vec_x
        self.polar_vec_z = self.tracker_vec_z

    def rotate(self, x, y, z):
        self.tracker_vec_x = tm.rotateNormal(self.tracker_vec_x, x, y, z)
        self.tracker_vec_z = tm.rotateNormal(self.tracker_vec_z, x, y, z)

    def rotateZ(self, x):
        self.tracker_vec_z = tm.rotateAroundAxis(self.tracker_vec_z, self.tracker_vec_x, x)
        self.c_rotation += x

    def track(self, angle):
        self.tracker_vec_x = tm.rotateAroundAxis(self.tracker_vec_x, self.polar_vec_x, -angle)
        self.tracker_vec_z = tm.rotateAroundAxis(self.tracker_vec_z, self.polar_vec_x, -angle)


    def getA(self):
        #return np.arctan2(self.tracker_vec_x[1], self.tracker_vec_x[0]) * 180/np.pi
        #return np.arccos(self.tracker_vec_x[0]) * 180/np.pi -90
        #return np.arctan2(self.tracker_vec_x[1], self.tracker_vec_x[0]) * 180/np.pi
        #print(np.sqrt(pow(self.tracker_vec_x[0],2) + pow(self.tracker_vec_x[1], 2) + pow(self.tracker_vec_x[2],2)))
        return np.sign(self.tracker_vec_x[1])*np.arccos(self.tracker_vec_x[0]/(np.sqrt(pow(self.tracker_vec_x[0], 2) + pow(self.tracker_vec_x[1], 2)))) * 180/np.pi

    def getB(self):
        #return np.arctan2(self.tracker_vec_x[2], self.tracker_vec_x[1]) * 180/np.pi
        #return np.arccos(self.tracker_vec_x[2]) * 180/np.pi -90
        #return np.arctan2(self.tracker_vec_x[2], self.tracker_vec_x[0]) * 180/np.pi
        return np.arccos(self.tracker_vec_x[2]) * 180/np.pi - 90

    def getC(self):
        #return np.arccos(self.tracker_vec_z[0]) * 180/np.pi - 90
        #return np.arctan2(self.tracker_vec_z[2], self.tracker_vec_z[1]) * 180/np.pi - 90
        #return np.sign(self.tracker_vec_z[2])*np.arccos(self.tracker_vec_z[0]/(np.sqrt(pow(self.tracker_vec_z[0], 2) + pow(self.tracker_vec_z[2], 2)))) * 180/np.pi - 90
        #return -np.sign(self.tracker_vec_z[1])*np.arccos(self.tracker_vec_x[0]/(np.sqrt(pow(self.tracker_vec_z[0], 2) + pow(self.tracker_vec_z[1], 2)))) * 180/np.pi
        #return -np.sign(self.tracker_vec_z[1]) * np.arccos(np.dot(self.tracker_vec_z, self.polar_vec_z)) * 180/np.pi
        return 0

    def getRefVecX(self):
        return self.ref_vec_x

    def getRefVecZ(self):
        return self.ref_vec_z

    def getPolarVecX(self):
        return self.polar_vec_x

    def getPolarVecZ(self):
        return self.polar_vec_z

    def getTrackerVecX(self):
        return self.tracker_vec_x

    def getTrackerVecZ(self):
        return self.tracker_vec_z