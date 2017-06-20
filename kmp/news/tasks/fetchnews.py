

from django_cron import CronJobBase, Schedule
from news.tasks.article_utils import article_models


class FetchNewsJob(CronJobBase):

    RUN_EVERY_MINS = 30

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    # The attribute code is necessary for CronJobBase inherited object
    code = "news.tasks.fetchnews.FetchNewsJob"

    def do(self):
        articles = article_models()

