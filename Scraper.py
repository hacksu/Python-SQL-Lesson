import requests
from wikipedia import WikipediaPage
import sqlite3


response = requests.get("https://pageviews.wmcloud.org/topviews/yearly_datasets/en.wikipedia/2022.json")
data = response.json()
# print(data)

cleo = WikipediaPage("Cleopatra")
# print(cleo)

db = sqlite3.connect('wikipedia.db')
cursor = db.cursor()

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS pages (
#     title TEXT PRIMARY KEY,
#     content TEXT,
#     view_count INTEGER
# )''')

cursor.execute('''
CREATE VIRTUAL TABLE IF NOT EXISTS pages USING fts4 (
    title TEXT,
    content TEXT,
    view_count INTEGER
)
''')

data = data[1:5]

for ranked_page in data:
    article_title = ranked_page["article"]
    view_count = ranked_page["views"]
    page = WikipediaPage(article_title)
    content = page.content

    cursor.execute(
        'INSERT OR IGNORE INTO pages(title, content, view_count) VALUES (?, ?, ?)',
        (article_title, page.content, view_count)
    )
    print("inserted", article_title)

db.commit()

cleo = cursor.execute("SELECT content FROM pages WHERE title='Cleopatra'").fetchone()
print(cleo[0][0:100])

cleo = cursor.execute("SELECT content FROM pages WHERE content MATCH 'Egypt'").fetchone()
print(cleo[0][0:100])

cleo = cursor.execute("SELECT content FROM pages WHERE content MATCH 'Egypt Roman Caesar'").fetchone()
print(cleo[0][0:100])

cleo = cursor.execute("SELECT content FROM pages WHERE content MATCH '\"Queen of the Ptolemaic Kingdom \"'").fetchone()
print(cleo[0][0:100])
