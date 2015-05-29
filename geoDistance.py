import socket
import string
import httplib
import json
from math import ceil, radians, cos, sin, asin, sqrt

def geo_to(host):
    """
    Return the geographic distance to an ip address in km.
    """

    conn = httplib.HTTPConnection('freegeoip.net')

    conn.request('GET', '/json/%s' % (host))
    res =  json.loads(conn.getresponse().read())

    conn.request('GET', '/json/')
    me =  json.loads(conn.getresponse().read())

    conn.close()
    return haversine(float(res['latitude']), float(res['longitude']), float(me['latitude']), float(me['longitude']))

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees).
    """

    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 

    # 6367 km is the radius of the Earth
    km = 6367 * c
    return int(km)    

def compute(host):
	"""
	Compute the geographic distance and print out the result
	"""
	dest = socket.gethostbyname(host)
	geo = geo_to(dest)
	print 'Distance to %s (%s km)\n' % (host, geo)

if __name__ == '__main__':
	file = open("targets.txt", "r")
	targets = file.readline()
	while targets != '':
		targets = targets.rstrip('\n')
		targets = targets.rstrip('\r')
		compute(targets)
		targets = file.readline()