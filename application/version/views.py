from django.shortcuts import render
from django.http import HttpResponse
from version import models
from application import settings
from django.views.decorators.csrf import csrf_exempt


import os

# Create your views here.
@csrf_exempt
def project_edit(request, url):

	url = url.split("/")
	for el in url[2:]:
		url[1] += "/%s"%el
	if not url[1]:
		url[1] = "index.html"

	if request.method == 'POST':
		print request.POST
		return HttpResponse("got it")

	try:
		element = models.Project.objects.get(slug=url[0]);
		path = os.path.join(settings.BASE_DIR, "../public_html/media/%s"%url[0])
		filetype = open(os.path.join(settings.BASE_DIR, "../public_html/media/projects/%s/%s"%(url[0],url[1])),'r')
		print filetype
		return HttpResponse(filetype.read());
	except Exception, e:
		print e
		raise
		return HttpResponse(status=404)
