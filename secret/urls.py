from django.urls import path
from secret import views


urlpatterns = [
    path('secret/minimal/', views.minimal),
    path('secret/standard/', views.standard),
    path('secret/premium/', views.premium),
    path('secret/beastmode/', views.beast_mode),
]
