#!/usr/bin/python3
#Downoads a page/file from a URL 
#https://stackoverflow.com/questions/30229231/python-save-image-from-url/30229298
import requests

def download(url,filename):
	with open(filename, 'wb') as handler:
		img = requests.get(url,stream=True)
		for block in img.iter_content(1024):
			if not block:
				break
			handler.write(block)

download("https://i.imgur.com/zmJArJA.jpg","Wooloo.jpg")
