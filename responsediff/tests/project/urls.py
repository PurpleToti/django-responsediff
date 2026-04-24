from django.contrib import admin
from django.http import HttpResponse
from django.urls import path


def simple_view(request):
    return HttpResponse('<html><body><h1>Hello</h1><p>World</p></body></html>')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('simple/', simple_view),
]
