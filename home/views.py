from django.shortcuts import render,redirect
from .models import UrlInput,Stat
from .forms import UrlInputForm
import random
import string
from datetime import datetime
from django.contrib.gis.geoip2 import GeoIP2


# Create your views here.
def showHome(request):
    if(request.method =='POST'):
        form = UrlInputForm(request.POST) 
        if form.is_valid():
            post = form.save(commit = False) 
            post.shorten_url = randomStringDigit(8) 
            post.save()
        return render(request,'home.html',{'form' : form,'shortenedUrl' : post.shorten_url}) 

    form = UrlInputForm() 
    return render(request,'home.html',{'form' : form}) 


def randomStringDigit(args):
    lettersAndDigits = string.ascii_lowercase +string.digits + string.ascii_uppercase
    key =  ''.join(random.choice(lettersAndDigits) for i in range(args))
    # print(key)
    return key


def urlRedirect(request,keyCode):
    # print(keyCode)
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR') 

    
    
    requiredUrl = UrlInput.objects.get(shorten_url = keyCode)
    row_created = Stat(url_input_details =requiredUrl,ip_address = ip)   # object created for stat model 
    # requiredUrl.noOfHit += 1
    row_created.save()
    return redirect(str(requiredUrl.url))


def info(request,keyCode):
    data = UrlInput.objects.get(shorten_url = keyCode)
    args = {'keycode':keyCode,'data': data}
    return render(request,'info.html',args)

    