

from django_cron import CronJobBase, Schedule
from django.conf import settings
from datetime import datetime


class FetchNewsJob(CronJobBase):

    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "news.tasks.fetchnews.FetchNewsJob"

    def do(self):
        datafile = settings.BASE_DIR + "/news/tasks/datafile.txt"
        with open(datafile, 'a') as df:
            df.write("Task run at " + datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + "\n")
