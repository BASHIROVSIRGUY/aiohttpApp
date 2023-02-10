import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, BLOB, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class PictureTable(Base):
    __tablename__ = "image_processing_storage"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    in_img = Column(BLOB, nullable=False)
    out_img = Column(BLOB, nullable=False)
    img_type = Column(String, nullable=False)
    create_date = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('UserTable')


class UserTable(Base):
    __tablename__ = "users"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String, nullable=False, unique=True)
