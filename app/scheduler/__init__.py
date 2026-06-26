from apscheduler.schedulers.background import BackgroundScheduler
from app.scheduler.jobs import email_polling_job

def init_scheduler():
    scheduler = BackgroundScheduler()
    # Poll every 5 minutes
    scheduler.add_job(email_polling_job, 'interval', minutes=5, id='email_poll_job')
    scheduler.start()
    return scheduler

def shutdown_scheduler(scheduler):
    if scheduler and scheduler.running:
        scheduler.shutdown()
