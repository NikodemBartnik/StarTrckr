import TrackerMath as tm
import numpy as np
import datetime

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
    
    def altAzToRaDec(alt, az, current_time, latitude, longitude):
        alt_rad = np.radians(alt)
        az_rad = np.radians(az)
        
        lat_rad = np.radians(latitude)
        lon_rad = np.radians(longitude)
        
        J2000 = 2451545.0
        current_JD = J2000 + (current_time - datetime.datetime(2000, 1, 1)).total_seconds() / 86400.0
        
        S = current_JD - J2000
        T = S / 36525.0
        T0 = 6.697374558 + (2400.051336 * T) + (0.000025862 * T ** 2)
        T0 = T0 % 24
        UT = current_time.hour + current_time.minute / 60.0 + current_time.second / 3600.0
        LST = T0 + UT * 1.002737909
        LST = LST % 24
        HA = LST * 15 - np.degrees(az_rad)

        sin_dec = np.sin(alt_rad) * np.sin(lat_rad) + np.cos(alt_rad) * np.cos(lat_rad) * np.cos(np.radians(HA))
        dec = np.degrees(np.arcsin(sin_dec))
        
        cos_ra = (np.sin(alt_rad) - np.sin(lat_rad) * np.sin(np.radians(dec))) / (np.cos(lat_rad) * np.cos(np.radians(dec)))
        ra = LST * 15 - np.degrees(np.arccos(cos_ra))
        
        return ra, dec