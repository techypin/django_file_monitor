from django.shortcuts import render, redirect
from .models import *
from django.template.defaulttags import register

@register.filter
def convert_bytes(num):
	num = int(num)
	for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
		if num < 1024.0:
			return "%3.1f %s" % (num, x)
		num /= 1024.0

@register.filter
def count_file(folder):
	file = File.objects.filter(path=folder)
	return len(file)


def home(request):
	folders = Folder.objects.all().order_by('-date_modified')
	return render(request, 'index.html', {'folders':folders})

def file(request):
	files = File.objects.all().order_by('-date_modified')
	if request.GET.get('folder'):
		folder = request.GET.get('folder')
		folder = Folder.objects.get(path=folder)
		files = files.filter(path=folder).order_by('date_modified')
	return render(request, 'file.html', {'files':files})

def settings(request):
	settings = Settings.objects.all()
	if request.method == "POST":
		file = request.FILES['file']
		data = file.read().decode("utf-8")
		file_lines = data.split("\n")
		for line in file_lines:
			Settings.objects.create(path=line)
		redirect('settings')
	return render(request, 'settings.html', {'settings':settings})

def Update_setting(request, id, status):
	settings = Settings.objects.get(id=id)
	if status == "True":
		settings.status = False
	else:
		settings.status = True
	settings.save()
	return redirect('settings')