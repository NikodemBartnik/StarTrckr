import TrackerMath as tm
import numpy as np

class TrackerController:
    def __init__(self):
        self.origin_vec_y = np.array([0, 1, 0], dtype=np.longdouble)
        self.origin_vec_x = np.array([1, 0, 0], dtype=np.longdouble)
        self.origin_vec_z = np.array([0, 0, 1], dtype=np.longdouble)

        self.ref_vec_x = self.origin_vec_x
        self.ref_vec_y = self.origin_vec_y
        self.ref_vec_z = self.origin_vec_z       
    
        self.polar_vec_x = self.origin_vec_x
        self.polar_vec_y = self.origin_vec_y
        self.polar_vec_z = self.origin_vec_z

        self.tracker_vec_x = self.origin_vec_x
        self.tracker_vec_y = self.origin_vec_y
        self.tracker_vec_z = self.origin_vec_z
        

    def polarAlign(self):
        self.polar_vec_x = self.tracker_vec_x
        self.polar_vec_y = self.tracker_vec_x
        self.polar_vec_z = self.tracker_vec_z


    def rotateAltitude(self, a):
        self.tracker_vec_x = tm.rotateAroundAxis(self.tracker_vec_x, self.tracker_vec_y, a)

    def rotateAzimuth(self, a):
        self.tracker_vec_x = tm.rotateAroundAxis(self.tracker_vec_x, self.origin_vec_z, a)
        self.tracker_vec_y = tm.rotateAroundAxis(self.tracker_vec_y, self.origin_vec_z, a)
        self.tracker_vec_z = tm.rotateAroundAxis(self.tracker_vec_z, self.origin_vec_z, a)

        self.ref_vec_x = tm.rotateAroundAxis(self.ref_vec_x, self.origin_vec_z, a)
        self.ref_vec_y = tm.rotateAroundAxis(self.ref_vec_y, self.origin_vec_z, a)
        self.ref_vec_z = tm.rotateAroundAxis(self.ref_vec_z, self.origin_vec_z, a)

    def rotateField(self, x):
        self.tracker_vec_y = tm.rotateAroundAxis(self.tracker_vec_y, self.tracker_vec_x, x)
        self.tracker_vec_z = tm.rotateAroundAxis(self.tracker_vec_z, self.tracker_vec_x, x)


    def track(self, angle):
        self.tracker_vec_x = tm.rotateAroundAxis(self.tracker_vec_x, self.polar_vec_x, angle)
        self.tracker_vec_y = tm.rotateAroundAxis(self.tracker_vec_y, self.polar_vec_x, angle)
        self.tracker_vec_z = tm.rotateAroundAxis(self.tracker_vec_z, self.polar_vec_x, angle)

    def setReferencePosition(self, known_ra, known_dec):
        known_ra_rad = np.radians(known_ra * 15) 
        known_dec_rad = np.radians(known_dec)

        polaris_vec = np.array([
            np.cos(known_dec_rad) * np.cos(known_ra_rad),
            np.cos(known_dec_rad) * np.sin(known_ra_rad),
            np.sin(known_dec_rad)
        ])

        self.ref_vec_x = np.array([1, 0, 0], dtype=np.longdouble)
        self.ref_vec_y = np.array([0, 1, 0], dtype=np.longdouble)
        self.ref_vec_z = polaris_vec


    def getA(self):
        return np.sign(self.tracker_vec_x[1])*np.arccos(self.tracker_vec_x[0]/(np.sqrt(pow(self.tracker_vec_x[0], 2) + pow(self.tracker_vec_x[1], 2)))) * 180/np.pi


    def getB(self):
        return np.arccos(self.tracker_vec_x[2]) * 180/np.pi - 90


    def getC(self):
        angle = np.degrees(np.arctan2(np.linalg.norm(np.cross(self.ref_vec_z, self.tracker_vec_z)), np.dot(self.ref_vec_z, self.tracker_vec_z)))
        if((np.cross(self.ref_vec_z, self.tracker_vec_z)[0] < 0 or self.tracker_vec_x[0] < 0) and not (np.cross(self.ref_vec_z, self.tracker_vec_z)[0] <= 0 and self.tracker_vec_x[0] <= 0)):
            angle = -angle
        return angle


    def getRefVecX(self):
        return self.origin_vec_x

    def getRefVecZ(self):
        return self.origin_vec_z

    def getPolarVecX(self):
        return self.polar_vec_x

    def getPolarVecZ(self):
        return self.polar_vec_z

    def getTrackerVecX(self):
        return self.tracker_vec_x

    def getTrackerVecZ(self):
        return self.tracker_vec_z

    def getADms(self):
        d, m, s = self.__decimalToDms(self.getA())
        return f"{d}° {m}' {s}\""

    def getBDms(self):
        d, m, s = self.__decimalToDms(self.getB())
        return f"{d}° {m}' {s}\""

    def getCDms(self):
        d, m, s = self.__decimalToDms(self.getC())
        return f"{d}° {m}' {s}\""

    def __decimalToDms(self, decimal):
        degrees = int(decimal)
        minutes = int((decimal - degrees) * 60)
        seconds = round((((decimal - degrees) * 60) - minutes) * 60, 2)
        return (degrees, minutes, seconds)
    
    def calculateRA(self):
        tracker_proj_xy = self.tracker_vec_x.copy()
        tracker_proj_xy[2] = 0
        cos_angle = np.dot(self.polar_vec_x, tracker_proj_xy) / (np.linalg.norm(self.polar_vec_x) * np.linalg.norm(tracker_proj_xy))
        angle = np.arccos(cos_angle)
        
        if np.cross(self.polar_vec_x, tracker_proj_xy)[2] < 0:
            angle = 2 * np.pi - angle
        ra = np.degrees(angle)
        ra = ra % 360
        
        return ra

    def calculateDEC(self):
        cos_dec = np.dot(self.tracker_vec_x, self.polar_vec_z) / (np.linalg.norm(self.tracker_vec_x) * np.linalg.norm(self.polar_vec_z))
        dec = np.degrees(np.arccos(cos_dec))
        if self.tracker_vec_x[2] < 0:
            dec = -dec
        return dec - 90

    def getRA(self):
        ra_decimal = self.calculateRA()
        hours = int(ra_decimal / 15)
        minutes = int((ra_decimal / 15 - hours) * 60)
        seconds = round((((ra_decimal / 15 - hours) * 60) - minutes) * 60, 2)
        return f"{hours}h {minutes}m {seconds}s"

    def getDEC(self):
        dec_decimal = self.calculateDEC()
        degrees = int(dec_decimal)
        minutes = int((dec_decimal - degrees) * 60)
        seconds = round((((dec_decimal - degrees) * 60) - minutes) * 60, 2)
        return f"{degrees}° {minutes}' {seconds}\""