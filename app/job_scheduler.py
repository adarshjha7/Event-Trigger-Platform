from .extensions import db, scheduler 
from .models import Trigger, EventLog
from datetime import datetime, timedelta
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

def trigger_event(app, trigger_id, is_test=False, payload=None):
    """
    Log an event when a trigger fires.
    """
    with app.app_context():  
        trigger = Trigger.query.get(trigger_id)
        if trigger:
            event = EventLog(
                trigger_id=trigger.id,
                triggered_at=datetime.now(),
                payload=payload if payload else trigger.payload, 
                is_test=is_test, 
                state='active' 
            )
            db.session.add(event)
            db.session.commit()

def schedule_trigger(app, trigger):
    """
    Schedule a trigger based on its type and schedule.
    """
    if trigger.type != 'scheduled':
        return

    if trigger.schedule_type == 'fixed_time':
        hour, minute = map(int, trigger.schedule_value.split(':'))
        if trigger.is_recurring:
            scheduler.add_job(
                func=trigger_event,
                trigger=CronTrigger(hour=hour, minute=minute),
                args=[app, trigger.id],
                id=f'trigger_{trigger.id}'
            )
        else:
            # One-time job
            run_time = datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
            if run_time < datetime.now():
                run_time += timedelta(days=1)  # Schedule for tomorrow
            scheduler.add_job(
                func=trigger_event,
                trigger='date',
                run_date=run_time,
                args=[app, trigger.id],
                id=f'trigger_{trigger.id}'
            )

    elif trigger.schedule_type == 'fixed_interval':
        # Handle fixed_interval scheduling (e.g., every 10 seconds)
        interval = int(trigger.schedule_value)
        if trigger.is_recurring:
            # Recurring job (e.g., every 10 seconds)
            scheduler.add_job(
                func=trigger_event,
                trigger=IntervalTrigger(seconds=interval),
                args=[app, trigger.id],
                id=f'trigger_{trigger.id}'
            )
        else:
            # One-time job (e.g., trigger after 10 seconds)
            run_time = datetime.now() + timedelta(seconds=interval)
            scheduler.add_job(
                func=trigger_event,
                trigger='date',
                run_date=run_time,
                args=[app, trigger.id],
                id=f'trigger_{trigger.id}'
            )

def cleanup_old_logs(app):
    """
    Clean up event logs older than 48 hours.
    """
    with app.app_context():  # Ensure the function runs within the Flask app context
        old_logs = EventLog.query.filter(EventLog.triggered_at < datetime.now() - timedelta(hours=48)).all()
        for log in old_logs:
            db.session.delete(log)
        db.session.commit()
