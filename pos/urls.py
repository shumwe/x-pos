from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls,name="admin-site"),
    path("pos/", include("posApp.urls")),
    path("", RedirectView.as_view(url="pos")),
    path('login/', RedirectView.as_view(url="/pos/login"),name="redirect-login"),
]

if settings.DEBUG == True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "JULLIVAM HARDWARE"
admin.site.site_title = "POS"
admin.site.index_title = 'Welcome'