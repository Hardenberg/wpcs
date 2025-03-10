from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(DNS)
admin.site.register(Http)
admin.site.register(Setting)
admin.site.register(Wordpress)
admin.site.register(TLD)