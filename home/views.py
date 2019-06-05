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
    data_for_bar_graph =  infos.filter(url_hit_time__gte = last_7_days).extra(select = {'day': 'date(url_hit_time)'}).values('day').annotate(hits =Count('id')).order_by('day')

    # dictionary_comprehensions 
    # data_for_bar_graph_2 = {i['day']:i['hits'] for i in data_for_bar_graph}
    # pprint(data_for_bar_graph_2)

    values = []
    
    for i in data_for_bar_graph: 
        for value in i.values(): 
            values.append(value)
    

    date = []
    hits_no = []
    for i in range(0,len(values),2):
        date.append(values[i])
        hits_no.append(values[i+1])
    
    print(date)
    args = {'keycode':keyCode,'infos': infos,'data' : data,'date' : mark_safe(date),'hits_no' :hits_no}
    return render(request,'info.html',args)

