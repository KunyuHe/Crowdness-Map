from datetime import datetime

from app.utils.core import db


class UserLog(db.Model):
    __tablename__ = 'user_logs'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    session_start = db.Column(db.Date, default=datetime.now(), nullable=False)
    search_cnt = db.Column(db.Integer, default=0, nullable=False)
    session_end = db.Column(db.Date, nullable=False)
