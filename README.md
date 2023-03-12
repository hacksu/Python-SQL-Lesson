Prerequisites: Python, packages "requests" and "wikipedia" installed via pip, intructions to be added later

# SQLite via Python

SQL ("Structured Query Language") is a language for constructing and using databases that has been very popular for a long time. It was the third most-used programming language for all professional developers who responded to the Stack Overflow Developer Survey in 2022. The databases that you construct and use by writing SQL consists of tables with rows and columns in which you can store data persistently and retrieve later; the idea of a database is that it will store data behind the scenes that persists even if the program that uses data is closed and the computer its running on is turned on and off again; a database is usually basically a sophisticated way to save data to files.

A lot of SQL databases are maintained by database servers. These are applications, like MySQL and PostgreSQL, who store data as needed on behalf of a program or programs that someone like you has written. These are large, powerful programs that are built to process huge amounts of data very quickly, and often run on networked devices so that they can be used by user-facing programs on other computers or devices entirely.

When you just need a way to save a normal amount of data in a normal file, though, the easiest SQL solution is to create a database with SQLite, which is a library of code that can be run independently or as part of any other program to create database files, where you need them and when you need them. SQLite is the most widely-deployed database in the world; it is installed on every Android and Apple phone so that apps can use it to store data, and when you click "save" in many desktop apps, like the Balsamiq Wireframes program I'm using in HIC right now, what you're saving is actually just a SQLite database file with a custom file extension. It's everywhere once you know where to look. For example, functions for running SQLite code are built right into Python.

## Wikipedia

Let's say that tomorrow, civilization collapses. We need to rebuild the electrical grid, figure out how to grow food, and distract ourselves from the state of the world by reading about stoats and marmosets. It would be nice to have access to Wikipedia without the Internet, and storing Wikipedia articles in a SQLite database would be one of the most convenient and reliable ways to do that.

For this lesson, though, we probably don't want to download all of Wikipedia, which is like 20gb of data. Let's download the important pages. There's a website called Topviews that catalogues the most-viewed pages on Wikipedia; let's check out [their list for 2022](https://pageviews.wmcloud.org/topviews/?project=en.wikipedia.org&platform=all-access&date=last-year&excludes=).

So, not all of this seems maximally conducive to rebuilding civilization, but I don't actually know how to search for that, so whoops. This should do for now. We can get this same data in a machine-readable form by going to https://pageviews.wmcloud.org/topviews/yearly_datasets/en.wikipedia/2022.json .

JSON is a text-based format for storing and retrieving data. What we have here is an array of JSON objects, which just consist of a few or a bunch of labeled data items; here we can see an array of objects, each of which contains data items labeled with "article", "views", "mobile_percentage", and "rank". These labels should be pretty self-explanatory.

```json
[
  {
    "article": "Main Page",
    "views": 1853370729,
    "mobile_percentage": 56.89,
    "rank": 1
  },
  {
    "article": "Cleopatra",
    "views": 55882835,
    "mobile_percentage": 98.54,
    "rank": 2
  },
  {
    "article": "Jeffrey Dahmer",
    "views": 54850769,
    "mobile_percentage": 87.79,
    "rank": 3
  },
  {
    "article": "2022 Russian invasion of Ukraine",
    "views": 50314503,
    "mobile_percentage": 52.08,
    "rank": 4
  }
]
```

If anyone's curious, the article for the Egyptian ruler Cleopatra was very popular last year because Android phones recommend searching for her. The rest of these are probably pretty self-explanatory.

![](cleopatra.jpg)

We can download this article in Python:

```python
import requests

response = requests.get("https://pageviews.wmcloud.org/topviews/yearly_datasets/en.wikipedia/2022.json")
data = response.json()
print(data)
```

This gives us the data in the form of a list of Python dicts. A list is what it sounds like; it's like an array, it stores an ordered sequence of things. A dict is a thing you can make in Python to store arbitrary labeled data items quickly and easily. You can access data from lists by index and from dicts by label, like this:

```python
print(data[0])
print(data[0]["article"])
```

Downloading Wikipedia articles in Python is pretty easy if you use [the Python library called "Wikipedia"](https://github.com/goldsmith/Wikipedia). We can download Cleopatra's article and add to the flood:

```python
from wikipedia import WikipediaPage

cleo_page = WikipediaPage("Cleopatra")
print(cleo_page.content)
```

That's a lot of information. When rebuilding civilization, maybe we can start with ancient Egypt and continue from there.

Now that we have some access to some data, we can save it somewhere.
