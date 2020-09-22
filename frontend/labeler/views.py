# coding: utf-8


from django.shortcuts import render
from labeler.models import TLabelerState
import json


def submitLabelerDecision(state):
    TLabelerState.objects.create(state = state)
    return "OK"


def getAllLabels():
    result = []
    for obj in TLabelerState.objects.all():
        result.append(obj.state)
    return json.dumps(result)


def clearAllLabels():
    TLabelerState.objects.all().delete()
    return "OK"

