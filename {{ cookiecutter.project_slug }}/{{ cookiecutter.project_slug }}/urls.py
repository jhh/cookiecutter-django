from django.contrib import admin
from django.urls import include, path

from {{ cookiecutter.project_slug }}.views import home_page_view

urlpatterns = [
    path("", home_page_view, name="home_page"),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]