from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron',  hour='0, 12', minute='30')#to run at everyday at 00:30 and 12:30

scheduler.start()



#You can add new jobs or remove old ones on the fly as you please.
#
