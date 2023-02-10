import uuid

from sqlalchemy.dialects.postgresql import UUID, BYTEA
from sqlalchemy import Column, UniqueConstraint, String, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class PictureTable(Base):
    __tablename__ = "image_processing_storage"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    in_img = Column(BYTEA, nullable=False)
    out_img = Column(BYTEA, nullable=False)
    img_type = Column(String, nullable=False)
    create_date = Column(DateTime, server_default=func.now())
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    user = relationship('UserTable')

    __table_args__ = (
        UniqueConstraint('in_img', 'user_id'),
    )


class UserTable(Base):
    __tablename__ = "users"

    id: uuid.UUID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String, nullable=False, unique=True)
