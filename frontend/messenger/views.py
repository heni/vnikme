# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from messenger.models import TUser


def add_user(request):
    def validate_fields(alias, firstname, lastname, email, password, userpic):
        if not alias:
            return "alias"
        if not firstname:
            return "firstname"
        if not lastname:
            return "lastname"
        if not email:
            return "email"
        if not password:
            return "password"
        return None

    def validate_data(alias, email):
        if TUser.objects.filter(alias = alias):
            return "alias"
        if TUser.objects.filter(email = email):
            return "email"
        return None

    alias = request.GET.get("alias", "")
    firstname = request.GET.get("firstname", "")
    lastname = request.GET.get("lastname", "")
    email = request.GET.get("email", "")
    password = request.GET.get("password", "")
    userpic = request.POST.get("userpic", "")

    bad_field = validate_fields(alias, firstname, lastname, email, password, userpic)
    if bad_field:
        return HttpResponse("""{"result": "fail", "reason": "missing field (%s)"}""" % bad_field, content_type = "text/html")

    bad_field = validate_data(alias, email)
    if bad_field:
        return HttpResponse("""{"result": "fail", "reason": duplicate object (%s)}""" % bad_field, content_type = "text/html")

    try:
        user = TUser(alias = alias, firstname = firstname, lastname = lastname, email = email, password = password, userpic = userpic)
        user.save()
    except e:
        HttpResponse("""{"result": "fail", "reason": "error while adding user (%s)"}""" % e, content_type = "text/html")

    return HttpResponse("""{"result": "ok"}""", content_type = "text/html")


def list_users(request):
    objs = TUser.objects.all()
    result = []
    for obj in objs:
        result.append(obj.alias)
    return HttpResponse("<br \>\n".join(result), content_type = "text/html")


