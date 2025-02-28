from django.contrib import admin
from django.contrib.staticfiles import views as staticfiles
from django.urls import path, re_path

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^static/(?P<path>.*)$", staticfiles.serve),
]
