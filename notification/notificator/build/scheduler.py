from apscheduler.schedulers.background import BackgroundScheduler

from .time_action import on_time

sched = BackgroundScheduler()


def send_by_time():
    print("Executing Task...")
    on_time()


sched.add_job(send_by_time, 'interval', hours=1)

# Starts the Scheduled jobs
sched.start()