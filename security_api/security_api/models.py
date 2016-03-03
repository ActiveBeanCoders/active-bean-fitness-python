from __future__ import unicode_literals

from django.db import models


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
