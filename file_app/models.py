from django.db import models

class Folder(models.Model):
	name 				= models.CharField(max_length=200)
	path 				= models.CharField(max_length=999, unique=True)
	date_modified		= models.DateTimeField(auto_now=False, auto_now_add=False)
	size				= models.CharField(max_length=50)
	updated_at			= models.DateTimeField(auto_now_add=True)
	parent				= models.ForeignKey(
							'self',
							blank=True, 
							null=True , 
							on_delete=models.CASCADE, 
							related_name='children')
	def __str__(self):
		return self.name

	class Meta:
		unique_together = [['path', 'parent']]

class File(models.Model):
	name 				= models.CharField(max_length=200)
	path 				= models.ForeignKey(Folder,on_delete=models.SET_NULL, null=True)
	date_modified		= models.DateTimeField(auto_now=False, auto_now_add=False)
	size				= models.CharField(max_length=50)
	updated_at			= models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class Settings(models.Model):
	path 				= models.CharField(max_length=500)
	status				= models.BooleanField(default=False)
