"""
UserSession Model
JWT/Session management for authentication
"""

from app import db
from datetime import datetime
from sqlalchemy import CheckConstraint
import uuid


class UserSession(db.Model):
    """UserSession entity - manages user authentication sessions"""

    __tablename__ = 'user_sessions'

    sessionid = db.Column('session_id', db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    userid = db.Column('user_id', db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), 
                      nullable=False, index=True)
    tokenhash = db.Column('token_hash', db.String(255), nullable=False)
    ipaddress = db.Column('ip_address', db.String(45))  # Supports IPv6
    useragent = db.Column('user_agent', db.Text)
    expiresat = db.Column('expires_at', db.DateTime, nullable=False)
    createdat = db.Column('created_at', db.DateTime, default=datetime.utcnow, nullable=False)

    # Constraints
    __table_args__ = (
        CheckConstraint('expires_at > created_at', name='check_session_expiry'),
    )

    # Relationships
    user = db.relationship('User', backref='sessions')

    def is_valid(self):
        """Check if session is still valid"""
        return datetime.utcnow() < self.expiresat

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'session_id': self.sessionid,
            'user_id': self.userid,
            'ip_address': self.ipaddress,
            'expires_at': self.expiresat.isoformat() if self.expiresat else None,
            'created_at': self.createdat.isoformat() if self.createdat else None,
            'is_valid': self.is_valid()
        }

    def __repr__(self):
        return f'<UserSession {self.sessionid}>'
