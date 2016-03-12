# Data Service (Elasticsearch)

## manual search

    response = urllib.request.urlopen("http://localhost:9200/com.activebeancoders.entity/Activity/%s" % activityId)\
         .read().decode("utf-8")
    activity = json.loads(response)
    return Response(activity)

with this in the settings.py:

    REST_FRAMEWORK = {
        'DEFAULT_PARSER_CLASSES': (
            'rest_framework.parsers.JSONParser',
        )
    }


## TODO

* utilize connection pool

