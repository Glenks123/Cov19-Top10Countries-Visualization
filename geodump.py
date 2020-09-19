import sqlite3
import json
import codecs
import ssl

connection = sqlite3.connect('cov19stats.sqlite')
cur = connection.cursor()
#Create 2 cursors, one for inside the loop and one for outside
cur2 = connection.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS LatLng(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    Latitude TEXT,
    Longitude TEXT
);
''')

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

cur.execute('SELECT * FROM Locations')
fhand = codecs.open('where.js','w','utf-8')

fhand.write('myData = [\n')
count = 0

for row in cur:
    #The json data
    data = str(row[2].decode())
    #print(data)

    try:
        js = json.loads(str(data))
        #print(js)
    except:
        continue

    if not ('status' in js and js['status'] == 'OK'):
        continue

    lat = js['results'][0]['geometry']['location']['lat']
    lng = js['results'][0]['geometry']['location']['lng']
    #print(lat,lng)

    if lat == 0 or lng == 0:
        continue 

    thelocation = js['results'][0]['formatted_address']
    thelocation = thelocation.replace("'","")

    #print(thelocation)

    try:
        print('Location: {} Latitude: {} Longitude: {}'.format(thelocation,lat,lng))
        count += 1
        if count>1:
            #Here is writing the output into the JAVASCRIPT FILE
            fhand.write(",\n")
            output = "["+str(lat)+","+str(lng)+",'"+thelocation+"']"
            fhand.write(output)
    except:
        continue
    
    cur2.execute('''INSERT INTO LatLng (Latitude, Longitude) VALUES (?, ?)''',(lat,lng))

cur.execute('''CREATE TABLE IF NOT EXISTS Stats AS SELECT Country.countriess, Cases.casess, Deaths.deathss, LatLng.Latitude, LatLng.Longitude FROM Country, Cases, Deaths, LatLng WHERE Country.id = Cases.id and Country.id = Deaths.id and Country.id = LatLng.id''')

connection.commit()
fhand.write("\n];\n")
cur.close()
fhand.close()
print(count, "records written to where.js")
print('Open where.html to see the visualized data in the map!')