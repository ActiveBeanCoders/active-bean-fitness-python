from __future__ import unicode_literals

import json


class Activity:
    id = -1
    activity = None
    comment = None
    date = None
    dist_hour = None
    dist_min = None
    dist_sec = None
    distance = None
    unit = None
    user_id = -1

    def __init__(self, user_id, id=None, activity=None, comment=None, date=None, dist_hour=None, dist_min=None,
                 dist_sec=None, distance=None, unit=None):
        self.user_id = user_id
        self.id = id
        self.activity = activity
        self.comment = comment
        self.date = date
        self.dist_hour = dist_hour
        self.dist_min = dist_min
        self.dist_sec = dist_sec
        self.distance = distance
        self.unit = unit

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return self.__dict__


class ActivitySearchCriteria:
    simpleCriteria = {}

    def __init__(self, simpleCriteria):
        self.simpleCriteria = simpleCriteria

    def __str__(self):
        return str(self.simpleCriteria)
