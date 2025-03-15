from .extensions import db

class Trigger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)  # 'scheduled' or 'api'
    schedule_type = db.Column(db.String(50))  # 'fixed_time' or 'fixed_interval'
    schedule_value = db.Column(db.String(100))  
    is_recurring = db.Column(db.Boolean, default=False)  # True for recurring, False for one-time
    api_endpoint = db.Column(db.String(200))  # Only for API triggers
    payload = db.Column(db.JSON) 
    is_test = db.Column(db.Boolean, default=False) 

    def serialize(self):
        return {
            'id': self.id,
            'type': self.type,
            'schedule_type': self.schedule_type,
            'schedule_value': self.schedule_value,
            'is_recurring': self.is_recurring,
            'api_endpoint': self.api_endpoint,
            'payload': self.payload,
            'is_test': self.is_test
        }

class EventLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trigger_id = db.Column(db.Integer, db.ForeignKey('trigger.id'))
    triggered_at = db.Column(db.DateTime, nullable=False)
    payload = db.Column(db.JSON)
    is_test = db.Column(db.Boolean, default=False)
    state = db.Column(db.String(20), default='active')  

    def serialize(self):
        return {
            'id': self.id,
            'trigger_id': self.trigger_id,
            'triggered_at': self.triggered_at.isoformat(),
            'payload': self.payload,
            'is_test': self.is_test,
            'state': self.state 
        }
