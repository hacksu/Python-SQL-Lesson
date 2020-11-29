import sqlite3
import requests


db = sqlite3.connect('database.db3')
cursor = db.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS "post" (
    "subreddit" TEXT,
    "title" TEXT,
    "content" TEXT,
    "permalink" TEXT,
    "attachment" TEXT,
    PRIMARY KEY("permalink")
)''')


while(True):

    sub = input("Enter a subreddit name: ")

    url = "https://www.reddit.com/r/"+sub+".json"

    response = requests.get(url,headers = {'User-agent':'Hacksu Scraper'})

    if(not response.ok):
        print("Got Error code: "+str(response.status_code))
    else:
        data = response.json().get('data')['children']
        for x in data:
            info = x["data"]
            cursor.execute('''INSERT INTO post(subreddit, title, content, permalink, attachment) VALUES(?,?,?,?,?)''',
                           (info["subreddit"],info["title"],info["selftext"],info["permalink"],info["url"]))
        db.commit()
        print("Done!")
