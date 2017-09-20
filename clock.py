from apscheduler.schedulers.blocking import BlockingScheduler
import os

scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', minutes=1)
def timed_job():
    print("Run notifier")
    os.system("python main.py")

scheduler.start()
