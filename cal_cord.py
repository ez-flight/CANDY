import math

## Ellipsoid Parameters as tuples (semi major axis, inverse flattening)
grs80 = (6378137, 298.257222100882711)
wgs84 = (6378137, 298.257223563)


def geodetic_to_geocentric(lat, lon, h):
    """
    Compute the Geocentric (Cartesian) Coordinates X, Y, Z
    given the Geodetic Coordinates lat, lon + Ellipsoid Height h
    """
    a, rf = (6378137, 298.257223563)
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)
    N = a / math.sqrt(1 - (1 - (1 - 1 / rf) ** 2) * (math.sin(lat_rad)) ** 2)
    X = (N + h) * math.cos(lat_rad) * math.cos(lon_rad)
    Y = (N + h) * math.cos(lat_rad) * math.sin(lon_rad)
    Z = ((1 - 1 / rf) ** 2 * N + h) * math.sin(lat_rad)

    return X, Y, Z

def fromLatLong(lat, lon, h, a, f):
    b, c, e2, e12 = initSpher(a, f)
    cos_lat = math.cos(lat)
    n = c / math.sqrt(1. + e12 * cos_lat ** 2)
    p = (n + h) * cos_lat
    x = p * math.cos(lon)
    y = p * math.sin(lon)
    z = (n + h - e2 * n) * math.sin(lat)
    return (x, y, z)


def _test():
    lat = -59.95
    lon = -149.683333
    h = 12
    print(geodetic_to_geocentric(lat, lon, h))

if __name__ == "__main__":
    _test()