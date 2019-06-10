from django.shortcuts import render,redirect
from .models import UrlInput,Stat
from .forms import UrlInputForm
import random
import string
import json
from pprint import pprint
from datetime import datetime,timedelta
from django.contrib.gis.geoip2 import GeoIP2
from django.db.models import Count
from django.utils.safestring import mark_safe
import collections
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings
# import ipdb; ipdb.set_trace()
host = settings.HOST[0]

# Create your views here.
def showHome(request):
    if(request.method =='POST'):
        form = UrlInputForm(request.POST) 
        if form.is_valid():
            post = form.save(commit = False) 
            post.shorten_url = randomStringDigit(8) 
            post.save()
        return render(request,'home.html',{'form' : form,'shortenedUrl' : post.shorten_url,'host':host}) 

    form = UrlInputForm() 
    return render(request,'home.html',{'form' : form,'host':host}) 


def randomStringDigit(args):
    lettersAndDigits = string.ascii_lowercase +string.digits + string.ascii_uppercase
    key =  ''.join(random.choice(lettersAndDigits) for i in range(args))
    return key


def urlRedirect(request,keyCode):
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
    infos = data.stats.all()
    
    last_7_days = datetime.today() - timedelta(days = 7)
    data_for_bar_graph =  infos.filter(url_hit_time__gte = last_7_days).extra(select = {'day':'date(url_hit_time)'}).values('day').annotate(hits =Count('id')).order_by('day') 
  
     # dictionary_comprehensions 
    date_hits = {i['day']:i['hits'] for i in data_for_bar_graph}
    
    #date to compare
    required_date =[]
    for i in range(0,7):
        required_date.append((datetime.today().date()-timedelta(days =i)).strftime('%Y-%m-%d'))

    #inserting value 0 in dates which does not exist in the records
    for i in required_date:
        if i in date_hits.keys():
            pass 
        else: 
           date_hits[i] = 0 
    sorted_date_hits  = collections.OrderedDict(sorted(date_hits.items()))
 
    #extracting date and hits for graph
    date =[]
    hits_no =[]
    for key,value in sorted_date_hits.items():
        date.append(key)
        hits_no.append(value) 

    args = {'keycode':keyCode,'infos': infos,'data' : data,'date' : mark_safe(date),'hits_no' :hits_no,'host':host}
    return render(request,'info.html',args) 

@csrf_exempt
def api_request(request):
    if(request.method == 'POST'):

        urlpost = request.POST['url'] 
        shorten_code =randomStringDigit(8)
        shorten_url_post = "http://127.0.0.1:8000/"+ shorten_code

        data = {
            "long url" : urlpost,
            "short url": shorten_url_post 
        }
        new_row = UrlInput(url = urlpost,shorten_url = shorten_code)
        new_row.save()
        return JsonResponse(data)
    
