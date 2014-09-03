#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
#  Coded by A. J. 
#
# This script use a geo webservice to locate an ip address
# provided by arguments in a commandline.
#
# Licensed under GPLv2.
#
# Python version: 2.7.x
#

import urllib2
import sys
import json
import re
import traceback


def get_info(host):
    """Get localization information about a host."""
    url = "http://freegeoip.net/json/%s" % host
    valid_ip = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
    if not re.match(valid_ip, host):
        print("/!\ '%s' is not a valid IP, please enter a valid one! /!\\" % host)
        sys.exit(-1)
    try:
       request = urllib2.Request(url)
       response = urllib2.urlopen(request)
       return response
    except:
       print("/!\ An error has occured, more info bellow /!\\")
       print(traceback.format_exc())
       print("/!\ Quitting now! /!\\")
       sys.exit(-1)
        	 
def usage():
    print("{0} [ hostname | ip ] \n\t\tExample: {0} 173.194.37.64".format(sys.argv[0]))

def main():
    result = []
    if len(sys.argv) >= 2:
       result = get_info(sys.argv[1])
    else:
       usage()
       sys.exit(-1)
    info = json.load(result)
    # Delete all keys with empty values
    for k in info.keys():
        if not info[k]: del info[k]

    print("########    SHOWING LOCATION INFORMATION ABOUT HOST %s    ########" % sys.argv[1])
    print("\tCountry Code: %s" % info.get('country_code','Not available'))
    print("\tCountry: %s" % info.get('country_name', 'Not available'))
    print("\tRegion Code: %s" % info.get('region_code','Not available'))
    print("\tCity: %s" % info.get('city', 'Not available'))
    print("\tZip Code: %s" % info.get('zipcode', 'Not available'))
    print("\tLatitude: %s" % info.get('latitude', 'Not available'))
    print("\tLongitude: %s" % info.get('longitude', 'Not available'))
    print("\tMetro Code: %s" % info.get('metro_code','Not available'))
    print("\tArea Code: %s" % info.get('areacode', 'Not available'))
    lat, lon = info.get('latitude'), info.get('longitude')
    if lat and lon:
        map_url = "https://www.openstreetmap.org/#map=12/%s/%s" % (lat, lon) 
        print("See location of %s on map => %s" % (sys.argv[1], map_url))


if __name__ == "__main__":
    main()

