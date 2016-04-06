
# CrapCrawler
Is an application for periodically crawl some bazaars

**[About](./docs/about.md)**

**[Overview](./docs/overview.md)**

**[Executable files](./docs/executable.md)**


## Quick start

 1. Download CrapCrawler from Github via git

``` 
git clone https://github.com/gr/CrapCrawler.git
```

or like zip archive

```
curl https://github.com/gr/CrapCrawler/archive/master.zip
```

 2. Install CrapCrawler

```
python install.py -r etc/requirements.txt
```

 3. Initial database

```
./manage.py
```

 4. Run service

```
./init.py start
```

 5. Open http://localhost:8080
