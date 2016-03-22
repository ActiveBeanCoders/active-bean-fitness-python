from __future__ import unicode_literals

from django.db import models
from django.forms import model_to_dict


class ActivityModel(models.Model):
    id = models.BigIntegerField(primary_key=True)
    activity = models.CharField(max_length=255, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    dist_hour = models.BigIntegerField(blank=True, null=True, db_column='dist_hour')
    dist_min = models.BigIntegerField(blank=True, null=True, db_column='dist_min')
    dist_sec = models.BigIntegerField(blank=True, null=True, db_column='dist_sec')
    distance = models.FloatField(blank=True, null=True)
    unit = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.BigIntegerField(db_column='user_id')
    alltext = models.TextField(blank=True, null=True)

    def to_dict(self):
        return model_to_dict(self, exclude='alltext')

    def save(self, *args, **kwargs):
        ar = []
        if self.activity is not None: ar.append(self.activity)
        if self.comment is not None: ar.append(self.comment)
        if self.date is not None: ar.append(str(self.date))
        if self.dist_hour is not None: ar.append(str(self.dist_hour))
        if self.dist_min is not None: ar.append(str(self.dist_min))
        if self.dist_sec is not None: ar.append(str(self.dist_sec))
        if self.distance is not None: ar.append(str(self.distance))
        if self.unit is not None: ar.append(self.unit)
        if self.user_id is not None: ar.append(str(self.user_id))
        self.alltext = ' '.join(ar)
        super(ActivityModel, self).save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'activity'
