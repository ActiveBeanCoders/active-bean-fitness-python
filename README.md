# Overview

This project is a simple webapp implemented using a few Python microservices
and an existing MySQL database and Elasticsearch index.

## How to run the project

Here are the steps to run the Python microservices in this project.

### First-time setup notes
Install Python 3.5: https://www.python.org/downloads/

Upgrade pip: https://pip.pypa.io/en/stable/installing/#upgrading-pip
```
pip3.5 install -U pip
pip3 install virtualenv
```

### Start virtual environment

```
sh init.sh
```

### Run service

```
cd foo_project
sh run.sh
```

## Testing

```
python manage.py test
```

## TODO

* `next_id` is a bottleneck.  figure out a way around it. (mysql, es)
* https
* is base Activity class needed?

