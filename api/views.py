from django.shortcuts import render
from rest_framework import viewsets
from api.serializers import Shortenurl_serializer
from home.models import UrlInput

# Create your views here.
class api_shorten(viewsets.ModelViewSet):
    queryset = UrlInput.objects.all()
    serializer_class = Shortenurl_serializer



