from corona.models import db

class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.TEXT, nullable=False)
    checksum = db.Column(db.String(70), unique=True, nullable=False)
    def __repr__(self):
        return '<%d : %s>' % (self.id, self.filename)
