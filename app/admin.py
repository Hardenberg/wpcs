from django.contrib import admin
from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib import messages
from django.utils.html import format_html


admin.site.register(DNS)
admin.site.register(Http)
admin.site.register(Setting)
admin.site.register(Wordpress)
admin.site.register(TLD)
admin.site.register(CRM)
admin.site.register(Vendor)
admin.site.register(PHPVersion)