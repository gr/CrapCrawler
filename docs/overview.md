## Overview

### About Logic and State parts
On the index page you can read about follow terms:
- Search
- Ad
- Engine
- Manager

All of this terms have a python class realization and
an SQLAlchemy class wich represent database state over Object Relation Model.
So, we have Python class Engine with logic and
ORM Engine class with specifications about some Engine, stored in database.
This is implemented for each term.
(TODO Maybe later move logic to ORM class, but it's a bad practice)


### Scheduler-Controller-Engine strategy
Because of we have:
- a lot of Engines with a lot of Searches
- each Engine and Search have custom periodicity
- engines constraints are independent (if some engine wait for timeout, other one may work)
- time to page processing is not stable

I choose follow objectives to work:
- each engine have separate thread to work. It helps to keep Engine timeout
- we have just Engine to get Ads, but we need to store it. So we need a Controller
So, each Engine assotiate with Controller and separated to thread.
- now we have to pass Search tasks to Controller. Each controller have a queue of Searches.
When Search request gets, it will be processed one by one.


### Web interface
I assume, that would be more easy to develop and use python Web server.
Install enterprise Web server, configure it(makefew configs for different servers),
use intermediate technologies(uwsgi, fcgi) is too overkill.
If this project will be too popular, I'll improve this part. =)
But because of python-httpd use serve_forever() endless cycle,  it needs separate thread.


### Sheduler
Scheduler is a cron like python structure wich works on endless cycle.
Scheduler perform code, wich add Search tasks to Controller queues.
Each enabled Search + Engine have a job in Sheduler.
Due to Scheduler requires endless cycle, it spend one thread also.



### Common scheme
```
init.py ---\
           crawlerdaemon---\----scheduler
                           |
              /--------/---------------\-------------\
     controller1   controller2   controllerN      python-httpd
              |        |               |
          engine1    engine2         engineN
```

