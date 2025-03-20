from django.db import models

class DNS(models.Model):
    dns = models.CharField(max_length=200, null=False,blank=False, verbose_name="DNS")
    tld = models.CharField(max_length=10, null=False,blank=False, verbose_name="TLD")
    ip = models.CharField(max_length=200, null=False,blank=False, verbose_name="IP-Adress")
    date = models.DateTimeField(auto_now=True, verbose_name="Modified")

    def __str__(self):
        return self.hostname()
    
    def hostname(self):
        return self.dns + "." + self.tld
    
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
    has_security_txt = models.BooleanField(default=False)
    security_txt = models.CharField(max_length=200, verbose_name="security.txt",null=True,blank=True,)
    checked = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dnsId.hostname()
    
class Wordpress(models.Model):
    dnsId = models.ForeignKey(DNS, on_delete=models.CASCADE, verbose_name="ID")
    version = models.CharField(max_length=200, null=False, blank=False)
    user_enumeration = models.BooleanField(null =True)
    php = models.CharField(max_length=20, verbose_name='PHP-Version', null=True,blank=True,)
    date = models.DateTimeField(auto_now=True, verbose_name="Modified")

    def __str__(self):
        return "Wordpress " + self.version + " auf " + self.dnsId.hostname()

class TLD(models.Model):
    tld = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.tld

class Vendor(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    mail = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return "Vendor: " + self.name

class CRM(models.Model):
    dns = models.ForeignKey(DNS, on_delete=models.CASCADE)
    mail = models.CharField(max_length=200, null=False, blank=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name='Vendor', null=True, blank=True)

    def __str__(self):
        return self.dns.hostname() + " an " + self.mail
    
class PHPVersion(models.Model):
    version = models.CharField(max_length=20, primary_key=True)
    release_date = models.DateField()
    active_support = models.DateField()
    security_support = models.DateField()
    end_of_life = models.DateField()

    def __str__(self):
        return self.version
