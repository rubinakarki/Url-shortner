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
    requiredUrl = UrlInput.objects.get(shorten_url = keyCode)
    
    #getting visitor's ip and country 
    ip_add =  get_ip_address(request)
    g = GeoIP2()
    country_value = ''
    try:
        country_value = (g.country_name(ip_add))
    except: 
        print("Oops!  That was not available in database.Try again...")
        country_value = 'Not Available'
    
    
    row_created = Stat(url_input_details =requiredUrl,ip_address = ip_add,country = country_value)   # object created for stat model 
    row_created.save()
    return redirect(str(requiredUrl.url))


def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR') 
    return ip
    


def info(request,keyCode):
    data = UrlInput.objects.get(shorten_url = keyCode)
    infos = data.stats.order_by('url_hit_time')
    args = {'keycode':keyCode,'infos': infos,'data' : data}
    return render(request,'info.html',args)

