from celery import Celery
from .worker import *
import datetime
import celery

# app = Celery('tasks', broker='amqp://guest:guest@localhost')



@app.decorators.periodic_task(run_every=datetime.timedelta(minutes=1)) # here we assume we want it to be run every 5 mins
def myTask():
	job()
	print("Job Done")