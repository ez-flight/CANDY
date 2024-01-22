import skyfield.sgp4lib as sgp4lib
from astropy import coordinates as coord, units as u
from astropy.time import Time
from datetime import date, datetime

time =  559889620.293
# time- J2000 date
# p,v- vectors, result of SGP4 in TEME frame
date= datetime.datetime(2000, 1, 1, 12, 0) + datetime.timedelta(days=time - 2451545)
p_0 = [-3219.2205314217895, 2841.7432608552854, -5795.244631928768]
v_0 = [5.578288437467041, -2.398731696159303, -4.276547464171784]
# Conversion from TEME to ITRS    
p,v= sgp4lib.TEME_to_ITRF(time,np.asarray(p_0),np.asarray(v_0)*86400)
v=v/86400

# Conversion from ITRS to J2000    
now = Time(date)
itrs = coord.ITRS(p[0]*u.km, p[1]*u.km, p[2]*u.km, v[0]*u.km/u.s, v[1]*u.km/u.s, v[2]*u.km/u.s, obstime=now)
gcrs = itrs.transform_to(coord.GCRS(obstime=now))
#p,v=gcrs.cartesian.xyz.value,gcrs.velocity.d_xyz.value
print (gcrs)