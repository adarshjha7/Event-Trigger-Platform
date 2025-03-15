from flask_restful import Resource, Api, reqparse
from .models import Trigger, EventLog
from . import db, scheduler
from datetime import datetime, timedelta
from .job_scheduler import trigger_event, schedule_trigger
from apscheduler.jobstores.base import JobLookupError


def init_routes(app):
    api = Api(app)

    # Create a new API trigger
    class APITriggerResource(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('api_endpoint', type=str, required=True)  # API endpoint to trigger
            parser.add_argument('payload', type=dict, required=True)  # Payload for the API trigger
            parser.add_argument('is_test', type=bool, default=False)  # True for test triggers
            args = parser.parse_args()

            # Create a trigger of type 'api'
            trigger = Trigger(
                type='api',
                api_endpoint=args['api_endpoint'],
                payload=args['payload'],
                is_test=args['is_test']
            )
            db.session.add(trigger)
            db.session.commit()

            return {'message': 'API trigger created successfully', 'id': trigger.id}, 201

    class ScheduledTriggerResource(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('schedule_type', type=str, required=True, choices=['fixed_time', 'fixed_interval'],
                               help="Schedule type must be 'fixed_time' or 'fixed_interval'.")
            parser.add_argument('schedule_value', type=str, required=True,
                               help="For 'fixed_time', use 'HH:MM' format (e.g., '15:00'). For 'fixed_interval', use an integer representing seconds (e.g., '10').")
            parser.add_argument('is_recurring', type=bool, default=False,
                               help="Set to True for recurring triggers, False for one-time triggers.")
            parser.add_argument('payload', type=dict, default={},
                               help="Payload for the trigger (optional).")
            parser.add_argument('is_test', type=bool, default=False,
                               help="Set to True for test triggers (optional).")
            args = parser.parse_args()

            # Validate schedule_value based on schedule_type
            if args['schedule_type'] == 'fixed_time':
                try:
                    hour, minute = map(int, args['schedule_value'].split(':'))
                    if not (0 <= hour < 24 and 0 <= minute < 60):
                        return {'message': "Invalid time. Hour must be 0-23, and minute must be 0-59."}, 400
                except ValueError:
                    return {'message': "Invalid schedule_value for fixed_time. Expected format: 'HH:MM' (e.g., '15:00')."}, 400
            elif args['schedule_type'] == 'fixed_interval':
                try:
                    interval = int(args['schedule_value'])
                    if interval <= 0:
                        return {'message': "Interval must be a positive integer (e.g., '10' for 10 seconds)."}, 400
                except ValueError:
                    return {'message': "Invalid schedule_value for fixed_interval. Expected format: integer (e.g., '10' for 10 seconds)."}, 400

            trigger = Trigger(
                type='scheduled',
                schedule_type=args['schedule_type'],
                schedule_value=args['schedule_value'],
                is_recurring=args['is_recurring'],
                payload=args['payload'],
                is_test=args['is_test']
            )
            db.session.add(trigger)
            db.session.commit()

            try:
                schedule_trigger(app, trigger)
            except ValueError as e:
                db.session.delete(trigger)
                db.session.commit()
                return {'message': str(e)}, 400

            return {'message': 'Scheduled trigger created successfully', 'id': trigger.id}, 201

    class TriggerResource(Resource):
        def get(self):
            return {'triggers': [trigger.serialize() for trigger in Trigger.query.all()]}

    class TestTriggerResource(Resource):
        def post(self, trigger_id):
            trigger = Trigger.query.get(trigger_id)
            if not trigger:
                return {'message': 'Trigger not found'}, 404

            if trigger.type == 'api':
                # Manually trigger API trigger
                trigger_event(app, trigger.id)
                return {'message': 'API trigger fired manually for testing'}, 200

            elif trigger.type == 'scheduled':
                trigger_event(app, trigger.id)
                return {'message': 'Scheduled trigger fired manually for testing'}, 200

            return {'message': 'Unsupported trigger type'}, 400

    class EventLogResource(Resource):
        def get(self):
            logs = EventLog.query.all()
            return {'logs': [{
                'id': log.id,
                'trigger_id': log.trigger_id,
                'triggered_at': log.triggered_at.isoformat(),
                'payload': log.payload,
                'is_test': log.is_test,
                'state': log.state
            } for log in logs]}

    class EditTriggerResource(Resource):
        def put(self, trigger_id):
            parser = reqparse.RequestParser()
            parser.add_argument('type', type=str)  
            parser.add_argument('schedule_type', type=str)  
            parser.add_argument('schedule_value', type=str)  
            parser.add_argument('is_recurring', type=bool)  
            parser.add_argument('api_endpoint', type=str)  
            parser.add_argument('payload', type=dict)  
            parser.add_argument('is_test', type=bool) 
            args = parser.parse_args()

            trigger = Trigger.query.get(trigger_id)
            if not trigger:
                return {'message': 'Trigger not found'}, 404

            # Update trigger fields
            for key, value in args.items():
                if value is not None:
                    setattr(trigger, key, value)

            db.session.commit()

            if trigger.type == 'scheduled':
                try:
                    scheduler.remove_job(f'trigger_{trigger.id}')
                except JobLookupError:
                    pass

                schedule_trigger(app, trigger)

            return {'message': 'Trigger updated successfully', 'id': trigger.id}, 200

    api.add_resource(APITriggerResource, '/api/triggers')  # API triggers
    api.add_resource(ScheduledTriggerResource, '/scheduled/triggers')  # Scheduled triggers
    api.add_resource(TriggerResource, '/triggers')  # List all triggers
    api.add_resource(TestTriggerResource, '/triggers/<int:trigger_id>/test')  # Manually trigger a trigger
    api.add_resource(EventLogResource, '/event_logs')  # List event logs
    api.add_resource(EditTriggerResource, '/triggers/<int:trigger_id>')  
