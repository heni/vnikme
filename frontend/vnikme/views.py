# coding: utf-8


from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.six.moves.urllib.parse import parse_qsl, urlparse, urlunparse
from django.utils.cache import patch_cache_control
from django.views.decorators.csrf import csrf_exempt
import httplib
import life.views


def do_general(request, body, params = {}):
    t = get_template("general.html")
    params["body"] = body
    html = t.render(params)
    response = HttpResponse(html, content_type = "text/html")
    patch_cache_control(response, max_age=0)
    return response

def nature_page(request):
    return do_general(request, "nature.html")

def authors_page(request):
    return do_general(request, "authors.html")

def poetry_page(request):
    return do_general(request, "poetry.html")

def life_save_page(request):
    link = life.views.saveLifeState(request.GET.get("fields", ""))
    return HttpResponse(link, content_type = "text/html")

def life_load_page(request):
    data = life.views.loadLifeState(request.GET.get("link", ""))
    return HttpResponse(data, content_type = "text/html")

def life_page(request):
    return do_general(request, "life.html", {"link": request.GET.get("load", "")})

def main_page(request):
    return do_general(request, "main.html")

