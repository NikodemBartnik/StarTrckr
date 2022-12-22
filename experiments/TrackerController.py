import TrackerMath as tm
import numpy as np
import math


class TrackerController:
    def __init__(self):
        self.ref_vec_x = np.array([1, 0, 0], dtype=np.longdouble)
        self.ref_vec_y = np.array([0, 1, 0], dtype=np.longdouble)
        self.ref_vec_z = np.array([0, 0, 1], dtype=np.longdouble)

        self.tracker_vec_x = self.ref_vec_x
        self.tracker_vec_z = self.ref_vec_z

    def polarAlign(self):
        self.polar_vec_x = self.tracker_vec_x
        self.polar_vec_z = self.tracker_vec_z

    def rotate(self, x, y, z):
        self.tracker_vec_x = tm.rotateNormal(self.tracker_vec_x, x, y, z)
        #self.tracker_vec_z = tm.rotateNormal(self.tracker_vec_z, x, y, z)

    def rotateZ(self, x):
        self.tracker_vec_z = tm.rotateNormal(self.tracker_vec_z, x, 0, 0)

    def track(self, angle):
        self.tracker_vec_x = tm.rotateAroundAxis(self.tracker_vec_x, self.polar_vec_x, -angle)
        self.tracker_vec_z = tm.rotateAroundAxis(self.tracker_vec_z, self.polar_vec_x, -angle)


    def getA(self):
        #return np.round(np.arccos(np.dot(self.tracker_vec_x, self.ref_vec_z)) * 180/np.pi, 2) - 90
        #return np.arccos(np.clip(np.dot(self.tracker_vec_x, self.ref_vec_z), -1.0, 1.0)) * 180/np.pi - 90
        return np.arctan2(self.tracker_vec_x[1], self.tracker_vec_x[0]) * 180/np.pi

    def getB(self):
        #return np.round(np.arccos(np.dot(self.tracker_vec_x, self.ref_vec_y)) * 180/np.pi, 2) - 90
        #return np.arccos(np.clip(np.dot(self.tracker_vec_x, self.ref_vec_y), -1.0, 1.0)) * 180/np.pi - 90
        return np.arctan2(self.tracker_vec_z[1], self.tracker_vec_z[2]) * 180/np.pi

    def getC(self):
        #return np.round(np.arccos(np.dot(self.tracker_vec_z, self.ref_vec_x)) * 180/np.pi, 2) - 90
        #return np.arccos(np.clip(np.dot(self.tracker_vec_z, self.ref_vec_x), -1.0, 1.0)) * 180/np.pi - 90
        return np.arctan2(self.tracker_vec_x[0], self.tracker_vec_x[2]) * 180/np.pi - 90

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