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

## Testing via curl

There are various scripts in the project under the `curl_tests` subfolder that
can be used to hit REST endpoints of running python microservices.

## TODO

* populate alltext field on save, update (mysql)
* `next_id` is a bottleneck.  figure out a way around it. (mysql, es)
* figure out pythonic Activity.save() for Elasticsearch entities.
* https

