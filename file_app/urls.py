from django.contrib import admin
from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('file/', file, name="file"),
    path('manage_folders/', Manage_folders, name="manage_folders"),
    re_path(r'^manage_folders/(?P<id>[\w-]+)/(?P<status>[\w-]+)$', Update_folders, name="update_folders"),
    re_path(r'^manage_folders/(?P<id>[\w-]+)$', Delete_folders, name="delete_folders"),
] 