from __future__ import unicode_literals

from django.db import models


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

    def __str__(self):
        return str(self.id) + ': ' + self.activity + ' ' + str(self.distance) + ' ' + self.unit + ' on ' + str(
                self.date)

    # TODO: populate alltext field on save, update
    # this doesn't work...
    def save(self, *args, **kwargs):
        self.alltext = self.activity
        super(Activity, self).save(*args, **kwargs)
        # models.Model.save(self, *args, **kwargs)

    class Meta:
        managed = False
        db_table = 'activity'


class ActivitySearchCriteria:
    simple_criteria = {}

    def __str__(self):
        return str(self.simple_criteria)
