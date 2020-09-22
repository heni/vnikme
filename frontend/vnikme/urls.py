"""vnikme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
#from django.contrib import admin
import vnikme.views
import life.views
import messenger.urls


urlpatterns = [
    url(r'^nature.*', vnikme.views.nature_page),
    url(r'^authors.*', vnikme.views.authors_page),
    url(r'^poetry.*', vnikme.views.poetry_page),
    url(r'^life_save.*', vnikme.views.life_save_page),
    url(r'^life_load.*', vnikme.views.life_load_page),
    url(r'^life.*', vnikme.views.life_page),
    url(r'^snake.*', vnikme.views.snake_page),
    url(r'^ttt.*', vnikme.views.ttt_page),
    url(r'^counter.*', vnikme.views.counter_page),
    url(r'^labeler_get_all.*', vnikme.views.labeler_get_all_page),
    url(r'^labeler_clear_all.*', vnikme.views.labeler_clear_all_page),
    url(r'^labeler_decision.*', vnikme.views.labeler_decision_page),
    url(r'^labeler.*', vnikme.views.labeler_page),
] + messenger.urls.urlpatterns + [
    url(r'^.*', vnikme.views.main_page),
]

