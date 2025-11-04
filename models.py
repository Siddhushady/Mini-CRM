# models.py
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Lead(db.Model):
    __tablename__ = 'leads'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    source = db.Column(db.String(100), nullable=True)   # e.g., website, referral
    status = db.Column(db.String(50), nullable=False, default='new')  # new, contacted, qualified, converted, lost
    score = db.Column(db.Integer, nullable=False, default=0)  # 0-100
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'email': self.email, 'phone': self.phone,
            'source': self.source, 'status': self.status, 'score': self.score,
            'notes': self.notes, 'created_at': str(self.created_at), 'updated_at': str(self.updated_at)
        }
