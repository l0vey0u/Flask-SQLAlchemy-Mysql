from corona.models import db

class DailyConfirmed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, unique=True, nullable=False)
    count = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return '<%s : %d>' % (self.date, self.count)
