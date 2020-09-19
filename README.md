# Cov19-Top10Countries-Visualization

This project visualizes the Top 10 countries with most covid cases using google maps geoJson API.
Hello, this is just a small project I have been working on during the weekend. 
In this project you will first run 'data_scrape.py'. In this file, the data is scraped from 'https://www.corona-cases.org/' I scrape data such as country, cases and deaths and store them in a sqlite database. The next file to run is 'geoload.py'. In this file I loop through all the countries in the database, then use google's geoJson API to get the json data for each country. I make a seperate table and store the data here. The last file to run is 'geodump.py'. In this file, i parse through the json data for each country then get data such as latitude and longitude and store them in a javascript file. The html page then visualizes the data in the javascript file on google maps.

First run 'data_scrape.py' > 'geoload.py' > 'geodump.py' 
