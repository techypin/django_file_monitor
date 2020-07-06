# Create your tasks here
from __future__ import absolute_import, unicode_literals
from .worker import *
import datetime
import celery

@celery.decorators.periodic_task(run_every=datetime.timedelta(minutes=1)) # here we assume we want it to be run every 5 mins
def myTask():
	job()
	print("Job Done")