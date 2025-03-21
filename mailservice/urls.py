from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailTemplateViewSet

router = DefaultRouter()
router.register(r'email_templates', EmailTemplateViewSet)

urlpatterns = [
    path('mailservice/', include(router.urls)),
]
