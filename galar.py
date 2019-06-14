#!/usr/bin/python3

#This script reads from https://www.serebii.net/swordshield/galarpokedex.shtml, keeping tabs on
#the current Galar pokedex; the whitelist of pokemon in the next games
#Reads generation data from pkmnGens.csv

import lxml.html as lh
import requests, re, csv

#Gets pokemon data from CSV
data = {}
with open('data/pkmnGens.csv',mode='r') as infile:
	reader = csv.reader(infile)
	data = dict((rows[0],rows[1]) for rows in reader)

#Vars
total = 0
gens = [0,0,0,0,0,0,0,0]	
strs = ["","","","","","","",""]
faves = ["Celebi","Quilava","Murkrow","Swellow","Furfrou","Smeargle","Dunsparce","Infernape"]
faveStr = ""

#Gets the data
page = lh.fromstring(requests.get("https://www.serebii.net/swordshield/galarpokedex.shtml").content)
mons = page.xpath('//table/tr/td[@class="fooinfo"]/a[starts-with(@href, "/pokemon/")]/text()')

#Iterates through each pokemon, and uses it as an index for the dict
for mon in mons:
	if re.match(r'[A-Za-z]',mon[0]):
		total += 1
		try:
			gen = int(data[mon]) - 1
			gens[gen] += 1
			strs[gen] += mon + "\n"
			#Checks if any of my favorites has been added yet
			if mon in faves:
				faveStr += mon + " has been added!\n"
		except:
			gens[7] += 1
			strs[7] += mon + "\n"

#Prints the data
print ("-"*30)
for i in range(8):
	print ("Generation: " + str(int(i) + 1) )
	print ("-"*30)
	print (strs[i])
	print ("-"*30)
print("Total pokemon: " + str(total))

if faveStr != "":
	print(faveStr[:-1])
else:
	print("No faves added yet :c")
print ("-"*30)
