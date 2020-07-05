from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('file/', file, name="file"),
    path('settings/', settings, name="settings"),
    re_path(r'^settings/(?P<id>[\w-]+)/(?P<status>[\w-]+)$', Update_setting, name="update_setting"),
] 