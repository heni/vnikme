# coding: utf-8


from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.six.moves.urllib.parse import parse_qsl, urlparse, urlunparse
from django.utils.cache import patch_cache_control
from django.views.decorators.csrf import csrf_exempt
import httplib
import life.views
import labeler.views
import urllib2
import vnikme.covid


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

def snake_page(request):
    return do_general(request, 'snake_page.html')

def ttt_page(request):
    return do_general(request, 'ttt_page.html')

def counter_page(request):
    answer = urllib2.urlopen("http://bots.baaas.org:5501").read()
    return HttpResponse(answer, content_type = "text/html")

def labeler_get_all_page(request):
    result = labeler.views.getAllLabels()
    return HttpResponse(result, content_type = "text/html")

def labeler_clear_all_page(request):
    result = labeler.views.clearAllLabels()
    return HttpResponse(result, content_type = "text/html")

def labeler_decision_page(request):
    result = labeler.views.submitLabelerDecision(request.GET.get("state", ""))
    return HttpResponse(result, content_type = "text/html")

def labeler_page(request):
    return do_general(request, 'labeler.html')

def do_covid_page(request, country_code):
    cases, deaths, last_ds = vnikme.covid.fetch_raw_cases_deaths(country_code)
    if not cases:
        cases, deaths = [0] * 8, [0] * 8
    avg_cases, avg_deaths = map(lambda x: vnikme.covid.rolling_average(x, 7), [cases, deaths])
    return do_general(
        request, 
        'covid.html',
        {
            'cases': list(map(int,cases[-37:])),
            'deaths': list(map(int,deaths[-37:])),
            'avg_cases': avg_cases[-30:],
            'avg_deaths': avg_deaths[-30:],
            'max_avg_cases_30': max(avg_cases[-30:]),
            'max_avg_deaths_30': max(avg_deaths[-30:]),
            'max_avg_cases': max(avg_cases),
            'max_avg_deaths': max(avg_deaths),
            'last_ds': last_ds
        }
    )

def covid_page(request):
    return do_covid_page(request, request.GET.get('country', 'GBR'))

def gbcovid_page(request):
    return do_covid_page(request, 'GBR')

def main_page(request):
    return do_general(request, "main.html")

