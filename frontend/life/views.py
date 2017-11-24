# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from life.models import TLifeState
import random


def generateRandomString(length):
    chars = "abcdefghijklmnopqrstuvwxyz"
    res = ""
    for i in xrange(length):
        res += chars[int(random.random() * len(chars))]
    return res


def isStateExists(link):
    objs = TLifeState.objects.filter(link = link)
    return len(objs) > 0


def saveLifeState(fields):
    link = ""
    while True:
        link = generateRandomString(10)
        if not isStateExists(link):
            break
    TLifeState.objects.create(link = link, data = fields)
    return link


def loadLifeState(link):
    objs = TLifeState.objects.filter(link = link)
    if len(objs)!= 1:
        return ""
    return objs[0].data

