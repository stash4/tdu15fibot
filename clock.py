from apscheduler.schedulers.blocking import BlockingScheduler
import os

scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', minutes=5, end_date='2017-10-02 10:59:59')
def timed_job():
    print("Run notifier")
    os.system("python main.py")

scheduler.start()
