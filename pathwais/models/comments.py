
from config.extensions import db 
from datetime import datetime
from sqlalchemy import ForeignKey, String, Text, DateTime, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, declared_attr

class BaseComment(db.Model):
    __tablename__ = "base_comments"
    __abstract__ = True 

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now())