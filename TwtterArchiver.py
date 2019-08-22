#!/usr/bin/python3
import lxml.html as lh
import requests, re, time, string, datetime
import sqlite3
import webbrowser

#Variables for twitter's date/time scheme
months = ('','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
#The current date
date = str(datetime.datetime.now().day)
if len(date) == 1:
        date = "0" + date
month = months[datetime.datetime.now().month]
year = str(datetime.datetime.now().year)[2:4]

#Gets a list of the most recent tweets made by a twitter account: Accepting their username as the argument
def getTweets(uName,archURL = ""):
    #List of tweets to return
    tweetList = list()
    
    #Request the twitter page
    #The intention is that this function use the uName to get the initial page, and the URL provided in 'archURL' when iterating back over the twitter account
    if archURL == "":
            page = lh.fromstring(requests.get("https://mobile.twitter.com/" + uName).content)
    else:
            page = lh.fromstring(requests.get(archURL).content)

    #Parse the html to get the 2 equal length lists. One being the tweet headers, and the other being the tweet containers
    headers = page.xpath('//tr[@class="tweet-header "]')
    tweets = page.xpath('//tr[@class="tweet-container"]')

    #Iterate through the tweet information
    for i in range(len(headers)):
        #Dict to append the tweet information into
        tweet = dict()

        #Get name of the tweet's poster
        name = headers[i].find('.//td[@class="user-info"]')
        name = bytetoASCII(headers[i])
        name = re.findall(r'@[^ ]+',name)[0]
        tweet['OP'] = name

        #Get url link to tweet
        url = headers[i].find('.//td[@class="timestamp"]/a').get("href")
        tweet['url'] = "https://www.twitter.com" + url

        #Get timestamp
        timestamp = headers[i].find('.//td[@class="timestamp"]/a')
        timestamp = bytetoASCII(timestamp)
        timestamp = twitterDateTime(timestamp)
        tweet['time'] = timestamp

        #Get tweet text
        text = tweets[i].find('.//div[@class="tweet-text"]/div')
        text = bytetoASCII(text)
        text = cleanse(text)
        tweet['text'] = text

        #Get reply div, and use regex to get a list of all users the tweet is replying to
        reply = tweets[i].find('.//div[@class="tweet-reply-context username"]')
        reply = bytetoASCII(reply)
        reply = re.findall(r'@[^ ]+',reply) #things like "@UserName42"
        tweet['replyingTo'] = cleanse(','.join(reply)) #Join that list of users into a comma separated string

        #Add the dict to the list of tweets
        tweetList.append(tweet)

    #Get URL of next page    
    nextURL = page.xpath('//div[@class="w-button-more"]/a/@href')
    if len(nextURL) > 0:
            nextURL = "http://mobile.twitter.com" + nextURL[0]
    else:
            nextURL = None
            #webbrowser.open(archURL)


    #Return list of tweets, and url to next page 
    time.sleep(1)
    return (tweetList, nextURL)

#Converts an htmlelement object to a utf-8 string
def bytetoASCII(data):
    if data != None:
        return cleanse(lh.tostring(data).decode("utf-8"))
    else:
        return ""

#Takes the odd twitter timestamps, and makes them be consistent
def twitterDateTime(string):
        #If in the format "10m","14h", or "3s", just use the current date
        if re.match(r'^[0-9]+[a-zA-Z]+$',string):
                return date + " " + month + " " + year
        #If in the format "Sep 4", flip the month and date, and place the current year on the end
        elif re.match(r'^[a-zA-Z]+ [0-9]+$',string):
                d = string.split(' ')
                if len(d[1]) == 1:
                        d[1] = "0" + d[1]
                return d[1] + " " + d[0] + " " + year
        #Else use their formatting of "17 Aug 18" (Fixing single digit days)
        else:
                d = string.split(' ')
                if len(d[0]) == 1:
                        d[0] = "0" + d[0]
                return(' '.join(d))

#Function that tidies up HTML strings, and removes characters that can be problematic with things like SQL
def cleanse(string):
	#Removes padding whitespace if exists
	string = string.strip()
	
	#Strips HTML tags from text (stuff like <div class="memes">)
	string = re.sub(r'<[^>]*>',"",string)
	
	#Strips character tags from text (&tab; and stuff like it)
	string = re.sub(r'&[#a-zA-Z0-9]+;',"", string)
	
	#Removes problematic characters from text (single quotes, backslashes, and newlines)
	string = string.replace("'","").replace("\\","-").replace("\n","")
	return string

#Nicely prints a retrieved list of tweets (used to test and see if this works)
def printTweets(tweetList):
        for tweet in tweetList[0]:
                print(tweet['OP'])
                print(tweet['text'])
                print("Replying to: " + tweet['replyingTo'])
                print(tweet['url'])
                print(tweet['time'])
                print('-'*40)

#Archives as far as ~3,200 tweets back from the given twitter account (The arbitrary limit of twitter's mobile site apparently)
def archiveTwitterAccount(uName,filename):
        #Counter for tweets archived total
        counter = 0
        
        #Get the initial page of tweets, add it to the DB, and increment the tweet counter
        t = getTweets(uName)
        writeToSQL(t[0],filename,uName)
        counter += len(t[0])
        print("Archiving @" + uName + ": " + str(counter))

        #While there's another page to tweets to be retrieved, repeat the process
        while t[1] != None:
                t = getTweets(None,t[1])
                writeToSQL(t[0],filename,uName)
                counter += len(t[0])
                print("Archiving @" + uName + ": " + str(counter))

#Transcribes tweets into an sqlite database file
def writeToSQL(tweetList,filename,uName):
        #Connect to the database file and create table for the account if it doesn't exist
        db = sqlite3.connect(filename)
        c = db.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS " + uName + " (OP TEXT, tweet TEXT, replyingTo TEXT, url TEXT, time TEXT)")

        #Write tweets to the table
        for tweet in tweetList:
                query = "INSERT INTO " + uName + " VALUES ('%s','%s','%s','%s','%s')" % (tweet['OP'],tweet['text'],tweet['replyingTo'],tweet['url'],tweet['time'])
                c.execute(query)
        
        #Save the database
        db.commit()

archiveTwitterAccount('Pokemon','twitter.sqlite')