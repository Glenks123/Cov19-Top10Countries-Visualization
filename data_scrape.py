from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
from urllib.request import Request, urlopen
import ssl
import sqlite3

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

connection = sqlite3.connect('cov19stats.sqlite')
cur = connection.cursor()

cur.executescript('''

    DROP TABLE IF EXISTS Country;
    DROP TABLE IF EXISTS Cases;
    DROP TABLE IF EXISTS Deaths;

    CREATE TABLE IF NOT EXISTS Country(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
        countriess
    );
    CREATE TABLE IF NOT EXISTS Cases(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
        casess INTEGER
    );
    CREATE TABLE IF NOT EXISTS Deaths(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
        deathss INTEGER
    );
''')

url = Request('https://www.corona-cases.org/', headers={'User-Agent': 'Mozilla/5.0'})
handle = urlopen(url).read()
soup = BeautifulSoup(handle, 'html.parser')

cases = soup.select('.home-item-column-short')
data = list()
for c in cases:
    c = c.getText().strip()
    data.append(c)
 
cases = data[2::2]
#print(cases)

deaths = data[3::2]
#print(deaths)

countries = soup.select('.stretched-link')
country_list = list()
for country in countries:
    country = country.getText().strip()
    country_list.append(country)

#print(country_list)

countries_by_cases = zip(country_list,cases)
countries_by_cases = dict(countries_by_cases)
#print(countries_by_cases)

countries_by_deaths = zip(country_list,deaths)
countries_by_deaths = dict(countries_by_deaths)
#print(countries_by_deaths)

clist = list()
for c in country_list:
    cur.execute('INSERT INTO Country(countriess) VALUES (?)',(c,))
    cur.execute('SELECT countriess FROM Country WHERE countriess = ?',(c,))

calist = list()
for k,v in countries_by_cases.items():
    cur.execute('INSERT INTO Cases(casess) VALUES (?)',(v,))
    cur.execute('SELECT casess FROM Cases WHERE casess = ?',(v,))
    
dlist = list()
for k,v in countries_by_deaths.items():
    cur.execute('INSERT INTO Deaths(deathss) VALUES (?)',(v,))
    cur.execute('SELECT deathss FROM Deaths WHERE deathss = ?',(v,))

print('Data succesfully scraped.')
print('Data Source: https://www.corona-cases.org/')

cur.close()
connection.commit()