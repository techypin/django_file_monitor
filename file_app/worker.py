from .models import *
import os
from datetime import datetime
from pprint import pprint
from django.utils import timezone
import time

def convert_bytes(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def get_stats(path):
	stat = os.stat(path)
	m_time = datetime.utcfromtimestamp(stat.st_mtime)
	size = stat.st_size
	return [m_time,size]

def get_data(folder_path):
	data = {}
	for root, dirs, files in os.walk(folder_path, topdown=False, followlinks=False):
		for name in dirs:
			if root not in data.keys():
				data[root]={}
				data[root]['name']=root.split('\\')[-1]
				m_time,folder_size=get_stats(root)
				data[root]['mtime']=m_time
				data[root]['size']=folder_size
				data[root]['parent']=None
				data[root]['files']=[]


			path = os.path.join(root, name)
			if path not in data.keys():
				data[path]  = {}
				data[path]['files']=[]
			
			m_time,folder_size = get_stats(path)
			data[path]['name']=name
			data[path]['mtime']=m_time
			data[path]['size']=folder_size
			data[path]['parent']=root

		for name in files:
			d={}

			path = os.path.join(root, name)
			if root not in data.keys():
				data[root]  = {}
				data[root]['files']=[]
			m_time,file_size=get_stats(path)
			d['name']=name
			d['path']=path
			d['mtime']=m_time
			d['size']=file_size
			data[root]['files'].append(d)
	new_data={}
	for i in sorted(data,key=len):
		new_data[i]=data[i]

	return new_data


def insert_data(data):
	for i in data:
		try:
			name = data[i]['name']
			path = i
			size = data[i]['size']
			mtime = data[i]['mtime']
			parent = data[i]['parent']
			folder_found=False
			

			if Folder.objects.filter(path=path).exists():

				folder=Folder.objects.get(path=path)
				if check_m_date(path,folder.date_modified):
					folder.date_modified=mtime
					folder.size = size
					folder.save()
					folder_found=True
				else:
					# print('>> skipping folder',folder.name)

					continue
			if not folder_found:
				if parent:
					try:
						parent=Folder.objects.get(path=parent)
					except:
						parent=None
				# print('\t\t'+name, path, mtime, size,">>>>",parent)

				folder = Folder.objects.create(
					name=name,
					path=path,
					date_modified=mtime,
					size=size,
					parent=parent
					)
			last_file_time=File.objects.filter(path=folder).order_by('-date_modified').first()

			for file in data[i]["files"]:
				file_name=file['name']
				file_path = file['path']
				file_m_time = file['mtime']
				file_size = file['size']
				file_found=False
				if last_file_time:
					if file_m_time < last_file_time.date_modified:
						# print("Here to skip the file >> ", file_name)
						continue
				if File.objects.filter(path=folder, name=file_name).exists():
					file=File.objects.get(path=folder, name=file_name)
					file.date_modified=file_m_time
					file.size = file_size
					file.save()
					file_found=True
				# print('\t\t'+file_name, file_path, file_m_time, file_size)
				if not file_found:
					File.objects.create(
					name=file_name,
					path=folder,
					date_modified=file_m_time,
					size=file_size,
					)
		except Exception  as err:
			print(err)
			# print(data[i])

f_path = "\\projects\\mom_blog"

def check_m_date(path,folder_l_time):
	if not folder_l_time:
		return True # apka phone off aa rka..of
	stat = os.stat(path)
	m_time = datetime.utcfromtimestamp(stat.st_mtime)
	# print(m_time)
	# print(folder_l_time)
	if m_time > folder_l_time:
		return True
	return False

def job():
	settings = Manage_folders.objects.filter(status=True)
	for i in settings:
		start=time.time()
		data = get_data(i.path)
		print(i.path,'\t scrape\t',time.time()-start)
		start=time.time()
		insert_data(data)
		print(i.path,'\t insert\t',time.time()-start)

