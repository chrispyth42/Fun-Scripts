# Fun-Scripts
A repo for fun scripts that I've written to perform neat tasks

### galar.py
Reads from the pokemon website 'Serebii.net' to keep tabs on currently known pokemon to be in the upcoming games; using data from 'pkmnGens.csv' to sort them by generation. Written because I'm still mildly upset that GameFreak announced not all pokes will be allowed to transfer, or even exist, in pokemon Sword/Shield. Existence in the Galar dex being the whitelist criteria :| 

### getNews.py
Reads from multiple news outlets' RSS feeds, and places the news stories into a local SQLite database file. With election season coming up, and controversy always surrounding news, data collected with this script might be fun to analyze

### download.py
Is a small but powerful function that accepts a URL to a webpage, and a destination filename, and downloads whatever data is on the target webpage into the file.

### RemoveSGUsers.ps1
Is called in the format .\RemoveUsers.ps1 CSV_PATH 'SG NAME' . It iterates through every user listed in a security group, and gets their full information using Get-ADUser. After doing so, it goes through each criteria in the CSV (see data\criteria.csv), and removes every user from the specified security group that has a property which equals that value. I'm fairly sure it's reliable, but it has NOT BEEN TESTED very extensively, so feel free to test and judge it before using it. In the sample CSV I've provided, it removes users named 'ike', as well as users that were created at that specific time, from the Security Group
