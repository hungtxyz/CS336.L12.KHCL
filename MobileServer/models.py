from config import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Boolean, default=False)
    inserted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    result = db.Column(db.String, default="none")
    def __repr__(self):
        return '<Task %r>' % self.id


