from django.contrib import admin
from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect
from django.urls import path, reverse
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib import messages
from django.utils.html import format_html

class DNSAdmin(admin.ModelAdmin):
    list_display = ('dns', 'tld', 'ip', 'date')
    search_fields = ('dns', 'tld', 'ip')
    list_filter = ('tld', 'date')
admin.site.register(DNS, DNSAdmin)

class HttpAdmin(admin.ModelAdmin):
    list_display = ('dnsId', 'http', 'https', 'has_security_txt', 'security_txt', 'checked')
    search_fields = ('dnsId__dns', 'dnsId__tld')
    list_filter = ('http', 'https', 'has_security_txt', 'checked')
admin.site.register(Http, HttpAdmin)

class SettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'date')
    search_fields = ('key', 'value')
    list_filter = ('date',)
admin.site.register(Setting, SettingAdmin)

class WordpressAdmin(admin.ModelAdmin):
    list_display = ('dnsId', 'version', 'user_enumeration', 'php', 'date', 'xml_rpc', 'open_directory')
    search_fields = ('dnsId__dns', 'dnsId__tld')
    list_filter = ('version', 'user_enumeration', 'php', 'date', 'xml_rpc', 'open_directory')
admin.site.register(Wordpress, WordpressAdmin)

class TLDAdmin(admin.ModelAdmin):
    list_display = ('tld',)
    search_fields = ('tld',)
admin.site.register(TLD, TLDAdmin)

class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'mail')
    search_fields = ('name', 'mail')
admin.site.register(Vendor, VendorAdmin)

class CRMAdmin(admin.ModelAdmin):
    list_display = ('dns', 'vendor')
    search_fields = ('dns__dns', 'dns__tld', 'vendor__name', 'vendor__mail')
    list_filter = ('vendor',)
admin.site.register(CRM, CRMAdmin)

class PHPVersionAdmin(admin.ModelAdmin):
    list_display = ('version',)
    search_fields = ('version',)
admin.site.register(PHPVersion, PHPVersionAdmin)