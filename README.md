# Fun-Scripts
A repo for one off, specific purpose scripts that I've written

### galar.py
Reads from the pokemon website 'Serebii.net' to keep tabs on currently known pokemon to be in the upcoming games; using data from 'pkmnGens.csv' to sort them by generation. Written because I'm still mildly upset that GameFreak announced not all pokes will be allowed to transfer, or even exist, in pokemon Sword/Shield. Existence in the Galar dex being the whitelist criteria :| 

### getNews.py
Reads from multiple news outlets' RSS feeds, and places the news stories into a local SQLite database file. With election season coming up, and controversy always surrounding news, data collected with this script might be fun to analyze

### download.py
Is a small but powerful function that accepts a URL to a webpage, and a destination filename, and downloads whatever data is on the target webpage into the file.

### TwtterArchiver.py
Accepts a username for a twitter account, and archives as far back as ~3,200 tweets into an SQLite database file (As far back as twitter's mobile site allows apparently). It turns out, twitter's mobile site is surprisingly unrestricted; having all of the tweet data neatly stored in the HTML, a link to the next page of tweets at the bottom of each page, and seemingly no limit on the amount of requests they allow you to make per second (I did put a 1 second delay between requests though just to be sure). The database file schema is (OP TEXT, tweet TEXT, replyingTo TEXT, url TEXT, time TEXT)

### ImgSite/
A fun little webpage with a single button on it, that loads in a random image from a pre-defined array of images; that image being positioned and scaled by CSS so that it's easily viewable on any screen. jQuery is definitely easier for accomplishing this sort of task, but I feel that it would have been a bit overkill to load the whole thing in, for a javascript that's only doing 1 thing
