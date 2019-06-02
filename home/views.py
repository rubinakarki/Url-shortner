from django.shortcuts import render,redirect
from .models import UrlInput
from .forms import UrlInputForm
import random
import string


# Create your views here.
def showHome(request):
    if(request.method =='POST'):
        form = UrlInputForm(request.POST) 
        if form.is_valid():
            post = form.save(commit = False) 
            post.shortenUrl = randomStringDigit(8) 
            post.save()
        return render(request,'home.html',{'form' : form,'shortenedUrl' : post.shortenUrl}) 

    form = UrlInputForm() 
    return render(request,'home.html',{'form' : form}) 


def randomStringDigit(args):
    lettersAndDigits = string.ascii_lowercase +string.digits + string.ascii_uppercase
    key =  ''.join(random.choice(lettersAndDigits) for i in range(args))
    # print(key)
    return key


def urlRedirect(request,keyCode):
    # print(keyCode)
    requiredUrl = UrlInput.objects.get(shortenUrl = keyCode)
    requiredUrl.noOfHit += 1
    requiredUrl.save()
    return redirect(str(requiredUrl))


def info(request,keyCode):
    data = UrlInput.objects.get(shortenUrl = keyCode)
    args = {'keycode':keyCode,'data': data}
    return render(request,'info.html',args)

    