"""
ModelImages Model
Stores images for car models
"""

from app import db
from datetime import datetime
from sqlalchemy import CheckConstraint


class ModelImage(db.Model):
    """ModelImage entity - images for car models (product photos, packaging, details)"""

    __tablename__ = 'model_images'

    imageid = db.Column('image_id', db.Integer, primary_key=True)
    modelid = db.Column('model_id', db.Integer, db.ForeignKey('car_models.model_id', ondelete='CASCADE'), 
                       nullable=False, index=True)
    imageurl = db.Column('image_url', db.Text, nullable=False)
    imagetype = db.Column('image_type', db.String(20))
    isprimary = db.Column('is_primary', db.Boolean, default=False)
    uploadedby = db.Column('uploaded_by', db.Integer, db.ForeignKey('users.user_id'))
    uploadedat = db.Column('uploaded_at', db.DateTime, default=datetime.utcnow, nullable=False)

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "image_type IN ('product', 'packaging', 'detail', 'user_photo')",
            name='check_image_type'
        ),
    )

    # Relationships
    carmodel = db.relationship('CarModel', backref='images')
    uploader = db.relationship('User', backref='uploaded_images')

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'image_id': self.imageid,
            'model_id': self.modelid,
            'image_url': self.imageurl,
            'image_type': self.imagetype,
            'is_primary': self.isprimary,
            'uploaded_by': self.uploadedby,
            'uploaded_at': self.uploadedat.isoformat() if self.uploadedat else None
        }

    def __repr__(self):
        return f'<ModelImage {self.imageid}: {self.imagetype}>'
