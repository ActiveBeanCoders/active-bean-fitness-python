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

    def __str__(self):
        return str(self.id) + ': ' + self.activity + ' ' + str(self.distance) + ' ' + self.unit + ' on ' + str(
                self.date)

    class Meta:
        managed = False
        db_table = 'activity'


""" This belongs in a python security_service
class DomainUser(models.Model):
    username = models.CharField(primary_key=True, max_length=255)
    comma_separated_roles = models.TextField()
    nickname = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'domain_user'


class DomainUserCredentials(models.Model):
    username = models.CharField(primary_key=True, max_length=255)
    password_hash = models.CharField(max_length=255, blank=True, null=True)
    salt = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'domain_user_credentials'
"""

