#!/usr/bin/env python
#############################################
#                                           #
#         Simple GeoIP Script               #
#	          by                              #
#               n3x07                       #
#   Visit http://netc0de.blogspot.com       #
#                                           #
#   Version 1.0  - Tested with: Python 2.7  #
#                                           #
#############################################

import urllib2
import sys
import json
import re


class GeoIP:
  def __init__(self, output="json"):
    """ Constructor of the class GeoIP """
    # freegeoip offer a free API for GeoIP
    self.url = "http://freegeoip.net/%s/" % output

  def validate_host(self, IP):
    """ VAlidate host by name or ip """
    # Cortesy of http://stackoverflow.com/questions/106179/regular-expression-to-match-hostname-or-ip-address
    ValidIpAddressRegex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
    ValidHostnameRegex = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
    if re.match(ValidHostnameRegex, str(IP)) or re.match(ValidIpAddressRegex, str(IP)):
      return True
    else:
      return False

  def getInfo(self, host):
    """ Get info about host """
    try:
      if not self.validate_host('google.com'):
         print "The IP or Hostname is not valid, please enter a valid one ;-)"
         sys.exit(2)  
      else:
         req = urllib2.Request(self.url+host)
         response = urllib2.urlopen(req)
         return response
    except Exception as e:
      print "An error has occured: {0}".format(e)
      sys.exit(2)
        	 
         

def usage():
  print """SimpleGeoIP [hostname | IP] 
              examples: SimpleGeoIP www.google.com
                        SimpleGeoIP 173.194.37.64"""

def main():
  """ Metodo main """
  result = []
  if len(sys.argv) > 2:
    handler = GeoIP(sys.argv[1])
    result = handler.getInfo(sys.argv[2])
  elif len(sys.argv) == 2:
    handler = GeoIP()
    result = handler.getInfo(sys.argv[1])
  else:
    usage()
    sys.exit(2)

  info = json.load(result)
  # Delete all keys with empty values
  for x in list(info.keys()):
    if info[x] == '':
        del info[x]
  print "=== SHOWING INFORMATION ABOUT ==="
  print "Country Code: %s" % info.get('country_code','Not available')
  print "Country: %s" % info.get('country_name', 'Not available')
  print "Region Code: %s" % info.get('region_code','Not available')
  print "City: %s" % info.get('city', 'Not available')
  print "Zip Code: %s" % info.get('zipcode', 'Not available')
  print "Latitude: %s" % info.get('latitude', 'Not available')
  print "Longitude: %s" % info.get('longitude', 'Not available')
  print "Metro Code: %s" % info.get('metro_code','Not available')
  print "Area Code: %s" % info.get('areacode', 'Not available')

if __name__ == "__main__":
    main()

  
