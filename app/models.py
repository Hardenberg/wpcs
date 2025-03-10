from django.db import models

class DNS(models.Model):
    dns = models.CharField(max_length=200, null=False,blank=False, verbose_name="DNS")
    tld = models.CharField(max_length=10, null=False,blank=False, verbose_name="TLD")
    ip = models.CharField(max_length=200, null=False,blank=False, verbose_name="IP-Adress")
    date = models.DateTimeField(auto_now=True, verbose_name="Modified")

    def __str__(self):
        return super().__str__()
    
    def hostname(self):
        return self.dns + '.'+ self.tld
    
class Setting(models.Model):
    key = models.CharField(max_length=200, null=False, blank=False)
    value = models.CharField(max_length=200, null=False, blank=False)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key

class Http(models.Model):
    dnsId = models.ForeignKey(DNS, on_delete=models.CASCADE)
    http = models.BooleanField()
    https = models.BooleanField()
    checked = models.DateTimeField(auto_now=True)

    def __str__(self):
        return super().__str__()
    
class Wordpress(models.Model):
    dnsId = models.ForeignKey(DNS, on_delete=models.CASCADE, verbose_name="ID")
    version = models.CharField(max_length=200, null=False, blank=False)
    user_enumeration = models.BooleanField(null =True)
    date = models.DateTimeField(auto_now=True, verbose_name="Modified")

    def __str__(self):
        return super().__str__()
    
    
    
class TLD(models.Model):
    tld = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.tld