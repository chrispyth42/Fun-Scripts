#!/usr/bin/python3
#This script aggregates news data from RSS feeds, clears the text of special string characters, and places each
#news story into an sqlite database file

import requests
import xml.etree.ElementTree as e
import sqlite3
import datetime
import re
import csv

#Accepts RSS feed url, and name of the station; to be appended onto each news story
#Returns a list of Dictionary objects, which are each a news story
def getNews(url,src,scope):
	#Return variable
	output = list()
	
	#Retrieves the data, exiting if connection fails
	try:
		page = requests.get(url) 
		data = e.fromstring(page.content)[0]
	except:
		print("Connection to " + src + " failed")
		return list()
		
	#Fetches all story items
	for elem in data.findall('.//item'):
		#Iterates through each attribute of the story items, and stores the data
		#Also clearing each string of single quotes and backslashes for database insertion
		headline = dict()
		for attr in list(elem):
			if attr.tag == "title":
				headline["title"] = cleanse(attr.text)
			if attr.tag == "description":
				headline["description"] = cleanse(attr.text)
			if attr.tag == "link":
				headline["link"] = attr.text.replace("'","").replace("\\","") #only do the necessary single quote and backslash removal for URLs
			if attr.tag == "pubDate":
				headline["date"] = cleanse(attr.text)[5:] #Trims off day of the week, and adds a 0 to the front to make it consistent if date number is only 1 char
				if headline["date"][1] == " ":
					headline["date"] = "0" + headline["date"]
				
		#Makes sure that it actually captured something before adding news station source, and appending it to output list 
		if headline != dict():
			#Ensures that an article has a publish date (to filter out ads)
			try:
				n = headline['date']
				headline["source"] = src
				headline["scope"] = scope
				output.append(headline)
			except:
				pass
				
	#print("Data retrieved from " + src)
	return output
	

#Just prints all the data collected with getNews()
def printNews(station):
	for elem in station:
		print(elem['title'])
		print("\t" + elem["description"])
		print("\t" + elem["link"])
		print("\t" + elem["date"])
		print("\t" + elem["source"])
		print("\t" + elem["scope"])
		print("--------------------------------")

#Accepts news story data, and the output database file location
def writeNews(station,file):		
	#Open and prep database file
	db = sqlite3.connect(file)
	c = db.cursor()
	c.execute("CREATE TABLE IF NOT EXISTS news (title TEXT, link TEXT, description TEXT, pubDate TEXT, capDate TEXT, source TEXT, scope TEXT)")
	
	#Counter for new news stories
	k = 0
	
	#For each news story, check to see if it's already in the database; if not, insert the new data
	for elem in station:
		c.execute("SELECT title,source FROM news WHERE title='%s' AND source='%s'" % (elem['title'],elem['source']))
		if (len(c.fetchall()) == 0):
			c.execute("INSERT INTO news VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (elem['title'],elem['link'],elem['description'],elem['date'],getDate(),elem['source'],elem['scope']))
			k += 1
	
	#Save the database
	db.commit()
	print(str(k) + " new news stories added\t" + getDate())

#Gets a formatted date string to use as a filename (In this case, 062019)
def getMY():
	m = str(datetime.datetime.now().month)
	if (len(m) == 1):
		m = "0" + m
	y = str(datetime.datetime.now().year)
	return m + y 

#Gets a formatted date string to add as news story retrieval time like:
# 06-22-2019 13:15
def getDate():
	m = str(datetime.datetime.now().month)
	if (len(m) == 1):
		m = "0" + m
	d = str(datetime.datetime.now().day)
	if (len(d) == 1):
		d = "0" + d
	y = str(datetime.datetime.now().year)
	
	hr = str(datetime.datetime.now().hour)
	if (len(hr) == 1):
		hr = "0" + hr
	min = str(datetime.datetime.now().minute)
	if (len(min) == 1):
		min = "0" + min
	return m + "-" + d + "-" + y + " " + hr + ":" + min
	
#Cleanses text of bad characters
def cleanse(string):
	#Removes leading space if exists
	string = string.strip()
	
	#Strips HTML tags from text
	string = re.sub(r'<[^>]*>',"",string)
	
	#Strips special characters from text (&tab; and stuff like it)
	string = re.sub(r'&[#a-zA-Z0-9]+;',"", string)
	
	#Removes problematic characters from text (single quotes, backslashes, and newlines)
	string = string.replace("'","").replace("\\","-").replace("\n","")
	
	return string
	
#Utilizes the other functions, and writes news from these feeds to a file
def writeFeeds():	
	allnews = list()
	
	#Try every entry in the news sources CSV, and print the name of each that gives an error
	f = open('/home/pi/Desktop/Share/News/data/newsSrc.csv')
	news = csv.reader(f)
	for row in news:
		try:
			allnews += getNews(row[0],row[1],row[2])
		except:
			print("Error in " + row[1])
			
	writeNews(allnews,"/home/pi/Desktop/Share/News/Store/" + getMY() + ".sqlite")

#Runs the script
writeFeeds()

#Printing a news source to test if it's working, before adding it to the csv
#printNews(getNews("https://news.yahoo.com/rss","Yahoo News","Global"))
