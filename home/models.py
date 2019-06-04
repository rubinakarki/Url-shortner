from django.db import models
from django.utils.timezone import now
# Create your models here.

class UrlInput(models.Model):
    url =  models.URLField(max_length=1000)
    shorten_url = models.CharField(max_length =1000,null =True,blank =True)
    created_at = models.DateTimeField(default= now,blank =True,null = True)
    
    def __str__(self):
        return '%s' %(self.shorten_url)

class Stat(models.Model):
    url_input_details = models.ForeignKey(UrlInput,on_delete =models.CASCADE,related_name = "stats")
    url_hit_time =  models.DateTimeField(default = now,blank =True,null =True)
    ip_address = models.CharField(blank =True ,null = True,max_length=15)
    country = models.CharField(blank =True ,null = True , max_length =50)

    def __str__(self):
        return '%s' %{self.url_input_details}

 
    

    
    
    




        