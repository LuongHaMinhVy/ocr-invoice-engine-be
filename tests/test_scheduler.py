import pytest
from app.scheduler import init_scheduler, shutdown_scheduler
from apscheduler.schedulers.background import BackgroundScheduler

def test_scheduler_initialization():
    scheduler = init_scheduler()
    assert isinstance(scheduler, BackgroundScheduler)
    assert scheduler.running is True
    
    # Check that the email_poll_job is registered
    job = scheduler.get_job('email_poll_job')
    assert job is not None
    assert job.id == 'email_poll_job'
    
    shutdown_scheduler(scheduler)
    assert scheduler.running is False
