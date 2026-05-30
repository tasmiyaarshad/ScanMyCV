from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from scanner import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('scan/', csrf_exempt(views.scan), name='scan'),
]