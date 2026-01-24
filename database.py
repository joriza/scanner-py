from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Ticker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100))
    sector = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    last_sync = db.Column(db.DateTime)

class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker_id = db.Column(db.Integer, db.ForeignKey('ticker.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    open = db.Column(db.Float)
    high = db.Column(db.Float)
    low = db.Column(db.Float)
    close = db.Column(db.Float)
    volume = db.Column(db.BigInteger)

    __table_args__ = (db.UniqueConstraint('ticker_id', 'date', name='_ticker_date_uc'),)

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
