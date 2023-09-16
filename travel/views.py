from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
	if (request.GET.get('source', None) and request.GET.get('dest', None)):
		print(request.GET.get('source'))
		return HttpResponse(request.GET['source'] + " " + request.GET['dest'])
	else:
		return HttpResponse("Please pass parameters properly!")
