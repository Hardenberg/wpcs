from django.urls import path
from . import views

urlpatterns =[
    path('', views.app, name="app"),
    path('dns', views.dns, name="dns"),
    path('wordpress', views.wordpress, name="wordpress")
]