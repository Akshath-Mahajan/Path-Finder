from django.shortcuts import render
from django.http import HttpResponse
def home(req):
    return render(req, 'Maps/maps_home.html')
def map(request):
    return render(request, 'Maps/maps_map.html')