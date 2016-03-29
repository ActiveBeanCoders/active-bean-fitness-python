from __future__ import unicode_literals

import json


class Activity:
    id = -1
    activity = None
    comment = None
    date = None
    distHour = None
    distMin = None
    distSec = None
    distance = None
    unit = None
    userId = -1

    def __init__(self, userId, id=None, activity=None, comment=None, date=None, distHour=None, distMin=None,
                 distSec=None, distance=None, unit=None):
        self.userId = userId
        self.id = id
        self.activity = activity
        self.comment = comment
        self.date = date
        self.distHour = distHour
        self.distMin = distMin
        self.distSec = distSec
        self.distance = distance
        self.unit = unit

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return self.__dict__


class ActivitySearchCriteria:
    simpleCriteria = {}

    def __init__(self, simpleCriteria=None):
        self.simpleCriteria = simpleCriteria
        if self.simpleCriteria is None:
            self.simpleCriteria = {}

    def __str__(self):
        return str(self.simpleCriteria)

