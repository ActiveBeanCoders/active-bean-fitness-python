## General setup notes
Installed Python 3.5: https://www.python.org/downloads/

Upgrade pip: https://pip.pypa.io/en/stable/installing/#upgrading-pip
```
pip3.5 install -U pip
pip3 install virtualenv
```

## Create virtual environment

Here are the steps that were taken to create the `fitness_env` virtual
environment packaged in this project:
```
python3.5 -m venv fitness_env
source fitness_env/bin/activate
pip install --upgrade pip
pip install django
pip install djangorestframework
pip install mysqlclient
pip install elasticsearch-dsl
export DYLD_LIBRARY_PATH=/usr/local/mysql/lib/
```

## After adding Activity model

```
python manage.py makemigrations hs
python manage.py sqlmigrate hs 0001
    BEGIN;
    --
    -- Create model Activity
    --
    CREATE TABLE `hs_activity` (`id` bigint NOT NULL PRIMARY KEY, `userId` bigint NOT NULL, `activity` varchar(256) NOT NULL, `date` datetime(6) NOT NULL, `unit` varchar(32) NOT NULL, `distance` numeric(10, 4) NOT NULL, `comment` varchar(4000) NOT NULL, `distHour` integer NOT NULL, `distMin` integer NOT NULL, `distSec` integer NOT NULL);

    COMMIT;
python manage.py migrate

python manage.py createsuperuser
    dan
    dandandan
```

## Import existing db model

```
python manage.py inspectdb
```
Then copied the results from the terminal into models.py.


## Testing via curl:
```
curl -H "Content-Type: application/json" -X POST -d '{"simple_criteria": {"fullText":"Laps"} }' http://localhost:9000/api/activity/search/ && echo
```

## Install your own code
How to install your own code into the virtualenv so it can be imported anywhere
in the same virtualenv, in any other project.

In your project that contains setup.py: `python setup.py develop`.  Then, to
use the installed module, for example:
```
python
from fitness_common import dantest
dantest.sayhello()
```

## TODO's

* Create and add Postman config for testing REST endpoints.
* Call another REST endpoint from service.  e.g. `data_all_service` calls `data_db_service` and `data_es_service`.
* Implement `data_es_service`.
* Implement `security_service`?
* Implement `gateway`?

