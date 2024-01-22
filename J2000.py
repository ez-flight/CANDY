from astropy import coordinates as coord
from astropy import units as u
from astropy.time import Time
from astropy import time

def position_GCRS_J2000 (now, xyz):
    cartrep = coord.CartesianRepresentation(*xyz, unit=u.km)
    gcrs = coord.ITRS(cartrep, obstime=now)
    itrs = gcrs.transform_to(coord.GCRS(obstime=now))
    loc = coord.EarthLocation(*itrs.cartesian.xyz)
    return loc


def _test():

    now = Time('2018-03-14 23:48:00')
    # position of satellite in GCRS or J20000 ECI:
    xyz=[-6340.40130292,3070.61774516,684.52263588]
    loc = position_GCRS_J2000(now,xyz)
    print(loc)


if __name__ == "__main__":
    _test()