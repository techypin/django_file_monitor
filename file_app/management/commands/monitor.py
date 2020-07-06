from django.core.management.base import BaseCommand
from file_app.worker import *
import time

class Command(BaseCommand):
    def handle(self, **options):
    	while True:
	    	job()
	    	print("[+] Job done\n")
	    	time.sleep(60*60)
