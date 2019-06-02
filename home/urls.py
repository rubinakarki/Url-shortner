from django.urls import path
from . import views

urlpatterns = [
    path('home/',views.showHome,name ="home"),
    path('<keyCode>',views.urlRedirect,name ="redirect"),
    path('stat/<keyCode>',views.info,name ="info")
]
