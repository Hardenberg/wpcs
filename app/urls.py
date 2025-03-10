from django.urls import path
from . import views
from .views import WordpressListView, DNSListView

urlpatterns =[
    path('', views.app, name="app"),
    path('dns', DNSListView.as_view(), name="dns"),
    path('wordpress', WordpressListView.as_view(), name='wordpress'),
    path('crm', views.crm, name="crm")
]