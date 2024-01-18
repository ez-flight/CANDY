import math

## Ellipsoid Parameters as tuples (semi major axis, inverse flattening)
grs80 = (6378137, 298.257222100882711)
wgs84 = (6378137., 1./298.257223563)


def geodetic_to_geocentric(lat, lon, h, af):
    """
    Compute the Geocentric (Cartesian) Coordinates X, Y, Z
    given the Geodetic Coordinates lat, lon + Ellipsoid Height h
    """
    a, rf = af
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    N = a / math.sqrt(1 - (1 - (1 - 1 / rf) ** 2) * (math.sin(lat_rad)) ** 2)
    X = (N + h) * math.cos(lat_rad) * math.cos(lon_rad)
    Y = (N + h) * math.cos(lat_rad) * math.sin(lon_rad)
    Z = ((1 - 1 / rf) ** 2 * N + h) * math.sin(lat_rad)
    return X, Y, Z

def initSpher(a, f):
    b = a * (1. - f)
    c = a / (1. - f)
    e2 = f * (2. - f)
    e12 = e2 / (1. - e2)
    return (b, c, e2, e12)

def fromLatLong(lat, lon, h, af):#Переход от геодезических координат к геоцентрическим
    a,f = af
    b, c, e2, e12 = initSpher(a, f)
    cos_lat = math.cos(lat)
    n = c / math.sqrt(1. + e12 * cos_lat ** 2)
    p = (n + h) * cos_lat
    x = p * math.cos(lon)/1000
    y = p * math.sin(lon)/1000
    z = (n + h - e2 * n) * math.sin(lat)/1000
    return (x, y, z)

def toLatLong(x, y, z, af): #Переход от геоцентрических координат к геодезическим
    a,f = af
    b, c, e2, e12 = initSpher(a,f)
    p = math.hypot(x, y)
    if p == 0.:
        lat = math.copysign(math.pi / 2., z)
        lon = 0.
        h = math.fabs(z) - b
    else:
        t = z / p * (1. + e12 * b / math.hypot(p, z))
        for i in range(2):
            t = t * (1. - f)
            lat = math.atan(t)
            cos_lat = math.cos(lat)
            sin_lat = math.sin(lat)
            t = (z + e12 * b * sin_lat ** 3) / (p - e2 * a * cos_lat ** 3)
        lon = math.atan2(y, x)
        lat = math.atan(t)
        cos_lat = math.cos(lat)
        n = c / math.sqrt(1. + e12 * cos_lat ** 2)
        if math.fabs(t) <= 1.:
            h = p / cos_lat - n
        else:
            h = z / math.sin(lat) - n * (1. - e2)
    return (lat, lon, h)


def _test():
    lat = 59.95
    lon = 30.316667
    h = 12
    X,Y,Z = geodetic_to_geocentric(lat, lon, h, wgs84)
    pr = math.sqrt((X**2)+(Y**2)+(Z**2))
    print(pr)
    X,Y,Z = fromLatLong(lat, lon, h, wgs84)
    pr = math.sqrt((X**2)+(Y**2)+(Z**2))
    print(pr)

if __name__ == "__main__":
    _test()