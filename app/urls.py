from django.urls import path
from . import views
from .views import WordpressListView, DNSListView, CRMListView

urlpatterns =[
    path('', views.app, name="app"),
    path('dns', DNSListView.as_view(), name="dns"),
    path('wordpress', WordpressListView.as_view(), name='wordpress'),
    path('crm', CRMListView.as_view(), name="crm"),
    path('create-crm', views.add_crm, name='create_crm_entry'),
    path('crm/<int:id>/', views.crm, name='crm_entry'),
]