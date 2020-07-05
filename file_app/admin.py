from django.contrib import admin
from .models import	*

@admin.register(Folder)
class folder_admin(admin.ModelAdmin):
	list_per_page = 400
	list_display = ('name','path','size', 'date_modified', 'parent','updated_at')



@admin.register(File)
class file_admin(admin.ModelAdmin):
	list_per_page=50
	list_display=('name','path','size', 'date_modified')

admin.site.register(Settings)


# Register your models here.
