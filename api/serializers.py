from rest_framework import serializers
from home.models import UrlInput

class Shortenurl_serializer(serializers.ModelSerializer):
    class Meta:
        model = UrlInput
        fields = ('url','shorten_url')