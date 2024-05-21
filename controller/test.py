from astropy.coordinates import EarthLocation, AltAz, SkyCoord
from astropy.time import Time
import astropy.units as u
import numpy as np

def altAzToRaDec(alt, az, latitude, longitude):
    # Convert altitude and azimuth to radians
    alt_rad = np.radians(alt)
    az_rad = np.radians(az)
    
    # Convert latitude and longitude to radians
    lat_rad = np.radians(latitude)
    lon_rad = np.radians(longitude)

    current_time = datetime.datetime.now()
    
    # Calculate current Julian date
    J2000 = 2451545.0
    current_JD = J2000 + (current_time - datetime.datetime(2000, 1, 1)).total_seconds() / 86400.0
    
    # Calculate local sidereal time (LST)
    S = current_JD - J2000
    T = S / 36525.0
    T0 = 6.697374558 + (2400.051336 * T) + (0.000025862 * T ** 2)
    T0 = T0 % 24
    UT = current_time.hour + current_time.minute / 60.0 + current_time.second / 3600.0
    LST = T0 + UT * 1.002737909
    LST = LST % 24
    
    # Calculate hour angle
    HA = LST * 15 - np.degrees(az_rad)
    
    # Calculate declination
    sin_dec = np.sin(alt_rad) * np.sin(lat_rad) + np.cos(alt_rad) * np.cos(lat_rad) * np.cos(np.radians(HA))
    dec = np.degrees(np.arcsin(sin_dec))
    
    # Calculate right ascension
    cos_ra = (np.sin(alt_rad) - np.sin(lat_rad) * np.sin(np.radians(dec))) / (np.cos(lat_rad) * np.cos(np.radians(dec)))
    ra = LST * 15 - np.degrees(np.arccos(cos_ra))
    
    return ra, dec

import datetime

# Define the altitude and azimuth coordinates
altitude = 50  # in degrees
azimuth = 1  # in degrees

# Define the current time
current_time = datetime.datetime.now()

# Define the location on Earth
latitude = 50.4672 
longitude = 18.7276 

# Call the function to convert alt-az to ra-dec
ra, dec = altAzToRaDec(altitude, azimuth, latitude, longitude)

# Print the resulting RA and DEC coordinates
print(f"RA: {ra} degrees, DEC: {dec} degrees")
