from config.extensions import db  
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import String, DateTime, ForeignKey, ARRAY, Index
from datetime import datetime


class Tag (db.Model):
    __tablename__ = "Tag"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    description: Mapped[str] = mapped_column( String(60), default="")
    created_at:Mapped[datetime] = mapped_column(
                                                DateTime(), 
                                                server_default=func.now()
                                                )
    update_at:Mapped[datetime] = mapped_column(
                                                DateTime(), 
                                                onupdate=func.now()
                                                )
    parent_id:Mapped[int] = mapped_column( ForeignKey("tags.id"))
    usage_count:Mapped[int] = mapped_column(default=0)
    is_active:Mapped[bool] = mapped_column(default=True)
    synonyms: Mapped[list[str]] = mapped_column(
        ARRAY(String), 
        default=list, 
        comment="Lista de sinónimos del tag"
    )

    
    __table_args__ = (
        Index("idx_tag_slug", slug),  
        Index("idx_tag_parent", parent_id),  
    )