from django.shortcuts import render
from django.http import HttpResponse
from version import models
from application import settings
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
from django.template.context_processors import csrf
from django.template.defaultfilters import slugify

from version.forms import UploadFileForm

import os,zipfile


def home(request):
	return render(request, 'home.html', {"projects":models.Project.objects.all()})

def project_edit(request, url):

	url = url.split("/")
	if len(url) < 2:
		#django redirect to url with / at end!
		pass
	for el in url[2:]:
		url[1] += "/%s"%el
	if not url[1]:
		url[1] = "index.html"

	if request.method == 'POST':
		try:
			edit_file(url[0],url[1],request.POST.get("count"),request.POST.get("content"))
		except Exception, e:
			print e
			raise
		return HttpResponse("got it")

	try:
		element = models.Project.objects.get(slug=url[0]);
		return render_to_request(request,url[0],url[1])
	except Exception, e:
		print e
		raise
		return HttpResponse(status=404)

def getFile(project,fileName):
	return open(os.path.join(settings.BASE_DIR, "../public_html/media/projects/%s/%s"%(project,fileName)),'r+')

def edit_file(project,fileName,count,data):
	print "\n===========\n%s\n%s\n%s\n%s"%(project,fileName,count,data)
	theFile = getFile(project,fileName)
	soup = BeautifulSoup(theFile.read(), 'html.parser')
	soup.find_all(class_="rw_editor")[int(count)].string = data

	theFile.seek(0)
	theFile.write(str(soup))
	theFile.truncate()
	theFile.close()
	return True

def render_to_request(request,project,fileName):
	theFile = getFile(project,fileName)
	if(".html" in fileName):		
		soup = BeautifulSoup(theFile.read(), 'html.parser')
		theFile.close()

		editor = soup.new_tag('script',src="/static/js/editor.js",type="text/javascript")
		csrf = soup.new_tag('input', id='csrftoken')
		soup.body.append(editor)
		return render(request, 'blank.html', {"data":str(soup)})
	return HttpResponse(theFile.read())


def project_new(request):
	return HttpResponse("new project")



def handle_uploaded_file(f,fileName):
	try:
		location = os.path.join(settings.BASE_DIR, "../public_html/media/projects_zipped/%s.zip"%fileName)
		with open(location, 'wb+') as destination:
			for chunk in f.chunks():
				destination.write(chunk)
		return location
	except Exception, e:
		print e
		raise



def project_new(request):
	if request.method == 'POST':
		print "\n"
		print request.FILES
		print request.POST
		form = UploadFileForm(request.POST, request.FILES)
		print form
		if form.is_valid():
			try:
				if models.Project.objects.get(slug=slugify(request.POST.get("title"))):
					return  HttpResponse("it failed, need a different title")
			except Exception, e:
				pass

			new_file = handle_uploaded_file(request.FILES['file'],slugify(request.POST.get("title")))
			destination = os.path.join(settings.BASE_DIR, "../public_html/media/projects/%s"%slugify(request.POST.get("title")))
			unzip(new_file, destination)
			project = models.Project(title=request.POST.get("title"))
			project.save()
			return  HttpResponse("it worked") #HttpResponseRedirect('/success/url/')
		return  HttpResponse("it failed") #HttpResponseRedirect('/success/url/')
	else:
		form = UploadFileForm()
		return render(request,'upload.html', {'form': form})

def unzip(source_filename, dest_dir):
	with zipfile.ZipFile(source_filename) as zf:
		for member in zf.infolist():
			# Path traversal defense copied from
			# http://hg.python.org/cpython/file/tip/Lib/http/server.py#l7

			words = member.filename.split('/')
			path = dest_dir
			for word in words[:-1]:
			# 	print "\t%s"%word
			# 	drive, word = os.path.splitdrive(word)
			# 	head, word = os.path.split(word)
				if word in (os.curdir, os.pardir, ''): continue
				path = os.path.join(path, word)
			# print "\t\t%s"%path

			if(member.filename.split('/').pop()): 
				member.filename = member.filename.split('/').pop() 
			zf.extract(member, path)