#!/usr/bin/python3
#Downoads a page/file from a URL 
#https://stackoverflow.com/questions/30229231/python-save-image-from-url/30229298
import requests

def download(url,filename):
	with open(filename, 'wb') as handler:
		#stream=True makes it so that it's downloaded in chunks instead of all at once: starting in the following line with .iter_content
		data = requests.get(url,stream=True)
		for block in data.iter_content(1024):
			if not block:
				break
			handler.write(block)

download("https://i.imgur.com/zmJArJA.jpg","Wooloo.jpg")
