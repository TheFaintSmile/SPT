from urllib import response
from django.shortcuts import render

def landingpage(request):
    return render(request, 'landingpage.html', response)