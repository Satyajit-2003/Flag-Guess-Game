from flask_sqlalchemy import SQLAlchemy
from app import app
import json

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    high_score = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<User %r>' % self.user_id

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    code = db.Column(db.String(2))
    flag = db.Column(db.String(100))

    def __repr__(self):
        return '<Country %r>' % self.country_name
    
def load_countries():
    with open(app.config['DATA_PATH']) as f:
        data = json.load(f)
        for country in data:
            db.session.add(Country(name=country['country'], code=country['code'], flag=country['flag']))

def get_random_country():
    return Country.query.order_by(db.func.random()).first()

def set_high_score(user_id, score):
    user = User.query.filter_by(user_id=user_id).first()
    if user.high_score < score:
        user.high_score = score
        db.session.commit()
        return True
    return False

with app.app_context():
    db.create_all()
    if not Country.query.all():
        load_countries()
    db.session.commit()

