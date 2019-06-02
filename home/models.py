from django.db import models
from django.utils.timezone import now
# Create your models here.

class UrlInput(models.Model):
    url =  models.URLField(max_length=1000)
    shortenUrl = models.CharField(max_length =1000,null =True,blank =True)
    noOfHit = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default= now,blank =True,null = True)
    ip_address =  models.PositiveIntegerField(blank = True,null= True)

    def __str__(self):
        return '%s' %(self.url)

