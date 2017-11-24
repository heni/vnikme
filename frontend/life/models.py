# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class TLifeState(models.Model):
    link = models.CharField(max_length = 15, db_index = True)
    data = models.TextField()

