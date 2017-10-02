from apscheduler.schedulers.blocking import BlockingScheduler
import os

scheduler = BlockingScheduler()


@scheduler.scheduled_job('interval', minutes=5, end_date='2017-10-02 11:10:00')
def timed_job():
    print('Run notifier')
    os.system('python main.py')


@scheduler.scheduled_job('cron', year=2017, month=10, day=2, hour=11, minute=15)
def scheduled_job():
    print('result')
    os.system('python result.py')


scheduler.start()
