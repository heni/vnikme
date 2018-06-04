# -*- coding: utf-8 -*-


from __future__ import unicode_literals
from django.db import models
import uuid


class TUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    alias = models.CharField(max_length = 64, db_index = True)
    firstname = models.TextField()
    lastname = models.TextField()
    email = models.EmailField()
    password = models.TextField()
    userpic = models.TextField()


class TThread(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(TUser)
    updatetime = models.BigIntegerField()


class TMessage(models.Model):
    time = models.BigIntegerField()
    content = models.TextField()
    thread = models.ForeignKey(TThread, on_delete=models.CASCADE)

