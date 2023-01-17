from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls,name="admin-site"),
    path("pos/", include("posApp.urls")),
    path("", RedirectView.as_view(url="pos")),
    path('login/', RedirectView.as_view(url="/pos/login"),name="redirect-login"),
]