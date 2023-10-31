from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    high_score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<User %r>' % self.user_id
    
with app.app_context():
    db.create_all()
    db.session.commit()