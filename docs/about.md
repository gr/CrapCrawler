# CrapCrawler is a crawler of a crap

The main idea is to periodically crawl some bazaars for an ads about some goods,
analyze results and make a notice if get something interesting.

Usual Ad ware is typical, it has: title, price, body; sometimes: date, pictures, other stuff

Typical scenario to work with bazaars is:
1) Make some search HTTP request
2) Get result with ad previews
3) If ad preview looks good, open original ad ware
4) If original ad ware also looks good make a decision.

I'll try to automate this process.

## Introduction of main terms.
### Search
Search is a term which contain:
- search query
- set of bazaars, what will be crawled
- search perform periodicity
- who and how need to be noticed

### Engine
Engine is a term to specify the method to get information from bazaar website.
It contains:
- bazaar name
- HTTP query string pattern of bazaar search with **query** and **pagination** patterns
- all about Ad fields: name, XPath, type of field
- page load periodicity, to don't DDOS bazaars

### Ad
Ad is a term to describe crawled ad ware, it contains:
- URL of ad ware, as a unique identification for ad ware
- title
- price
- all crawled fields from Engine

### Manager
Manager is a term to describe a person.
Some contacts information for notice messages.

## Abstract
So, as mentioned above, we need a software to periodically crawl
a number of bazaars by a number of searches, and make a notice if was found something interesting.
My usual stack is Linux & Python.
- CrapCrawler will made firstly for Linux, but hope it would be consistent for Windows & Mac OS too.
- Python is easy for mock ups, writing and understanding.
Also Python have no platform strict dependencies and hard work about environment and compilation.
- Service will work as a daemon. (Linux init script style has implemented)
- State will be store in sqlite3 database and handled via SQLAlchemy.
- Manipulation with software will be implemented via Web service.
For easy usage I'll use Python Web server. It's not enterprise, but free from problems with Web server configuration.
In case of performance or security troubles, we can use: lo interface, nginx as proxy, isolated environment(chroot, docker)
(Here I'll improve my knowledge about new JS frameworks and methodology=)
- To make decision about notice we need some metric.
I hope machine learning, artificial Intelligence, neural networks help us to make some predicts or clusters.
And this predicts will be a metric. Anyway I'll try to learn this methodical deeper.

Because of purposes of this project is not engineering only but research too.
I separate CrapCrawler processing to two parts: crawling and analyzing.
Crawling is a main part of CrapCrawler, it just store parsed adware to database.
Analyzing will be implemented with some plugins, which may analyze stored data different ways.
Research part is to try different ways to analyze via different plugins.

So, let's try =)
