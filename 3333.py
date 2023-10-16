from skyfield.api import EarthSatellite, load, wgs84

from read_TBF import read_tle_base_file, read_tle_base_internet

#from Tools.scripts.generate_re_casefix import alpha


ts = load.timescale(builtin=True)
 
 
name, L1, L2 = read_tle_base_internet(25544)
 
sat = EarthSatellite(L1, L2)
 
times = ts.now()
 
geocentric = sat.at(times)
 
print(geocentric.position.km)
 
#lat, lon = wgs84.subpoint_of(geocentric)
elevation_m = 123.0

#print('Latitude:', lat)
#print('Longitude:', lon)
#subpoint = wgs84.latlon(lat, lon, elevation_m)
#wsg84.subpoint_of()
#print(subpoint)
print(wgs84.subpoint_of(geocentric))
