import sys
import os
import time
import re
import json

try: # Python 3.x
    from urllib.parse import quote as urlencode
    from urllib.request import urlretrieve
except ImportError:  # Python 2.x
    from urllib import pathname2url as urlencode
    from urllib import urlretrieve

try: # Python 3.x
    import http.client as httplib
except ImportError:  # Python 2.x
    import httplib

# from astropy.table import Table
import numpy as np

import pprint
pp = pprint.PrettyPrinter(indent=4)

def mastQuery(request):
    """Perform a MAST query.

        Parameters
        ----------
        request (dictionary): The MAST request json object

        Returns head,content where head is the response HTTP headers, and content is the returned data"""

    server = 'mast.stsci.edu'

    # Grab Python Version 
    version = ".".join(map(str, sys.version_info[:3]))

    # Create Http Header Variables
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain",
               "User-agent": "python-requests/" + version}

    # Encoding the request as a json string
    requestString = json.dumps(request)

    print "\n\nHEADERS:\n"
    print headers

    print "\n\nREQUEST_STRING:\n"
    print requestString
    

    requestString = urlencode(requestString)

    # opening the https connection
    conn = httplib.HTTPSConnection(server)


    # Making the query
    conn.request("POST", "/api/v0/invoke", "request=" + requestString, headers)

    # Getting the response
    resp = conn.getresponse()
    head = resp.getheaders()
    content = resp.read().decode('utf-8')

    # Close the https connection
    conn.close()

    return head, content




objectOfInterest = 'M101'

resolverRequest = {'service':'Mast.Name.Lookup',
                     'params':{'input':objectOfInterest,
                               'format':'json'},
                     }

headers,resolvedObjectString = mastQuery(resolverRequest)

resolvedObject = json.loads(resolvedObjectString)

pp.pprint(resolvedObject)

objRa = resolvedObject['resolvedCoordinate'][0]['ra']
objDec = resolvedObject['resolvedCoordinate'][0]['decl']

objectOfInterest = 'M101'

resolverRequest = {'service':'Mast.Name.Lookup',
                     'params':{'input':objectOfInterest,
                               'format':'json'},
                     }

mastRequest = {'service':'Mast.Caom.Cone',
               'params':{'ra':objRa,
                         'dec':objDec,
                         'radius':10.0},
               'format':'json',
               'pagesize':2000,
               'page':1,
               'removenullcolumns':True,
               'removecache':True}

headers,mastDataString = mastQuery(mastRequest)

mastData = json.loads(mastDataString)

print "\nHEADERS:\n"
print headers

print "\nKEYS:\n"
print(mastData.keys())

print "\nDATA COUNT:\n"
print(len(mastData['data']))

print "\nFIRST DATA VALUE:\n"
pp.pprint(mastData['data'][0])

print("Query status:",mastData['status'])


def listCaomMissions():
    request = {
        'service':'Mast.Missions.List',
        'params':{},
        'format':'json'
    }
        
    headers,outString = mastQuery(request)
    
    outData = [x['distinctValue'] for x in json.loads(outString)['data']]
    
    return outData

print listCaomMissions()
