from __future__ import unicode_literals

import json

from django.db import models
from django.forms import model_to_dict


class Activity(models.Model):
    id = models.BigIntegerField(primary_key=True)
    activity = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    dist_hour = models.BigIntegerField(blank=True, null=True)
    dist_min = models.BigIntegerField(blank=True, null=True)
    dist_sec = models.BigIntegerField(blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.BigIntegerField()
    alltext = models.TextField(blank=True, null=True)

    def __init__(self, user_id, id=None, activity=None, comment=None, date=None, dist_hour=None, dist_min=None,
                 dist_sec=None, distance=None, unit=None):
        super().__init__()
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

    # TODO: populate alltext field on save, update
    # this doesn't work...
    def save(self, *args, **kwargs):
        self.alltext = self.activity
        super(Activity, self).save(*args, **kwargs)
        # models.Model.save(self, *args, **kwargs)

    def to_json(self):
        return json.dumps(self.__dict__)

    def to_dict(self):
        return model_to_dict(self, exclude='alltext')

    class Meta:
        managed = False
        db_table = 'activity'


class ActivitySearchCriteria:
    simple_criteria = {}

    def __str__(self):
        return str(self.simple_criteria)
