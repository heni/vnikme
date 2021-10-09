# coding: utf-8


from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.six.moves.urllib.parse import parse_qsl, urlparse, urlunparse
from django.utils.cache import patch_cache_control
from django.views.decorators.csrf import csrf_exempt
import life.views
import labeler.views
import urllib.request
import vnikme.covid
import vnikme.plots
import math
import json
import datetime
from django.template.defaulttags import register


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
    request = urllib.request.Request("http://bots.baaas.org:5501")
    answer = urllib.request.urlopen(request).read()
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
    cases, deaths, tests, location, jabs, last_ds = vnikme.covid.fetch_raw_cases_deaths(country_code)
    if not cases:
        cases, deaths, tests = [0] * 8, [0] * 8, [0] * 8
    prevalence = [min(float(cases[i]) / max(tests[i], 1), 1.0) for i in range(len(cases))]
    avg_cases, avg_deaths, avg_tests = map(lambda x: vnikme.covid.rolling_average(x, 7), [cases, deaths, tests])
    avg_prevalence = [min(float(avg_cases[i]) / max(avg_tests[i], 1), 1.0) for i in range(len(avg_cases))]
    cases_wow = [math.log((avg_cases[i] + 50.0) / (avg_cases[i - 7] + 50)) for i in range(7, len(avg_cases))]
    deaths_wow = [math.log((avg_deaths[i] + 5.0) / (avg_deaths[i - 7] + 5)) for i in range(7, len(avg_deaths))]
    cases_img = vnikme.plots.plot_to_png({'cases': avg_cases})
    deaths_img = vnikme.plots.plot_to_png({'deaths': avg_deaths})
    tests_img = vnikme.plots.plot_to_png({'tests': avg_tests})
    prevalence_img = vnikme.plots.plot_to_png({'prevalence': avg_prevalence})
    cases_wow_img = vnikme.plots.plot_to_png({'log_cases_wow': cases_wow})
    deaths_wow_img = vnikme.plots.plot_to_png({'log_deaths_wow': deaths_wow})
    jabs_img = vnikme.plots.plot_to_png({'jabs': jabs})
    return do_general(
        request, 
        'covid.html',
        {
            'cases': list(map(int,cases[-37:])),
            'deaths': list(map(int,deaths[-37:])),
            'avg_cases': avg_cases[-30:],
            'avg_deaths': avg_deaths[-30:],
            'jabs': jabs[-30:],
            'max_avg_cases_30': max(avg_cases[-30:]),
            'max_avg_deaths_30': max(avg_deaths[-30:]),
            'max_avg_cases': max(avg_cases),
            'max_avg_deaths': max(avg_deaths),
            'cases_img': cases_img,
            'deaths_img': deaths_img,
            'tests_img': tests_img,
            'prevalence_img': prevalence_img,
            'cases_wow_img': cases_wow_img,
            'deaths_wow_img': deaths_wow_img,
            'jabs_img': jabs_img,
            'location': location,
            'last_ds': last_ds,
        }
    )

def covid_page(request):
    return do_covid_page(request, request.GET.get('country', 'GBR'))

def gbcovid_page(request):
    return do_covid_page(request, 'GBR')

@register.simple_tag
def get_timus_tasks(data, coder, dt):
    return len(data[coder]['dates'].get(dt, []))

@register.simple_tag
def get_total_timus_tasks(data, coder):
    return data[coder]['count']

def timus_page(request):
    data = json.loads(open('/home/vnik/work/vnikme/frontend/vnikme/timus.json', 'rt').read())
    codes = sorted(data.keys(), key = lambda x: data[x]['name'])
    coders = [(coder, data[coder]['name']) for coder in codes]
    dates = []
    for i in range((datetime.date.today()-datetime.date(2021, 10, 1)).days+2):
        dt = (datetime.date(2021, 10, 1) + datetime.timedelta(days=i)).isoformat()
        dates.append(dt)
    return do_general(request, 'timus.html', {'coders': coders, 'dates': dates, 'data': data})

def main_page(request):
    return do_general(request, "main.html")

