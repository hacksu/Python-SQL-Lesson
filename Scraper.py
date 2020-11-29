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
cursor.execute('''
CREATE TABLE IF NOT EXISTS "comment" (
    "id" TEXT,
    "content" TEXT,
    "postlink" TEXT,
    "permalink" TEXT,
    FOREIGN KEY("postlink") REFERENCES "post",
    PRIMARY KEY("id")
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
            commentsReq = requests.get("https://www.reddit.com/" + info['permalink'] + ".json",headers = {'User-agent':'Hacksu Scraper'})
            if(not commentsReq.ok):
                print("Got Error code: "+str(commentsReq.status_code))
            else:
                comments = commentsReq.json()[1]['data']['children']
                for comment in comments:
                    if comment['kind'] != 'more':
                        cinfo = comment['data']
                        cursor.execute('''INSERT INTO comment(id, content, postlink, permalink) VALUES(?,?,?,?)''',(cinfo['id'], cinfo['body'], info['permalink'], cinfo['permalink']))
                        # print(comment['data']['body'])


        db.commit()
        print("Done!")
