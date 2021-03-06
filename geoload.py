import urllib.request, urllib.parse, urllib.error
from urllib.request import urlopen
import sqlite3
import ssl
import http
import sys
import json

api_key = False

if api_key is False:
    api_key = 42
    serviceurl = "## ENTER SERVICE URL HERE ##"
else :
    serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

connection = sqlite3.connect('cov19stats.sqlite')
cur = connection.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Locations(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    Address TEXT,
    geodata TEXT
);
''')


# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cur.execute('SELECT countriess FROM Country')
count = 0


for country in cur.fetchall():
    count += 1
    if count>=10:
        print('Retrieved top 10 locations with most covid cases!')
        break
    country = country[0].strip()
    #print(country)

    parms = dict()
    parms['query'] = country
    if api_key is not False:
        parms['key'] = api_key
    #Ex {'query': 'United States', 'key': 42}


    url = serviceurl + urllib.parse.urlencode(parms)
    #print(url)
    print('Retrieving {}'.format(url))

    openurl = urlopen(url, context=ctx)

    data = openurl.read().decode()
    print('Retrieved {} characters {}'.format(len(data),  data[:20].replace('\n',' ')))
    try:
        js = json.loads(data)
    except:

        print(data)
        continue  


    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS'):
        print('=== Failure To Retrieve ===')
        print(data)
        break

    cur.execute('''INSERT INTO Locations(Address, geodata) VALUES (?, ?)''',(memoryview(country.encode()),memoryview(data.encode())))

    connection.commit()

cur.close()
print('=== ALL DONE ===')
print('Run geodump.py to visualize the data on a map')
print('Make sure to open the sqlite databse to check the data.')

    
