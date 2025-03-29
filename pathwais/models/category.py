from config.extensions import db  
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import String, DateTime, ForeignKey, ARRAY,  Index
from datetime import datetime


class Category (db.Model):
    __tablename__ = "Category"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    description: Mapped[str] = mapped_column( String(60), default="")
    meta_title = Mapped[str] =  mapped_column( String(60), default="")
    created_at:Mapped[datetime] = mapped_column(
                                                DateTime(), 
                                                server_default=func.now()
                                                )
    update_at:Mapped[datetime] = mapped_column(
                                                DateTime(), 
                                                onupdate=func.now()
                                                )
    parent_id:Mapped[int] = mapped_column( ForeignKey("Category.id"))
    usage_count:Mapped[int] = mapped_column(default=0)
    is_active:Mapped[bool] = mapped_column(default=True)
    synonyms: Mapped[list[str]] = mapped_column(
        ARRAY(String), 
        default=list, 
        comment="synonymus list of Category"
    )
    children: Mapped[list["Category"]] = relationship(
        back_populates="parent", 
        lazy="dynamic"  
    )
    parent: Mapped["Category | None"] = relationship(
        back_populates="children", 
        remote_side=[id]  
    )

    __table_args__ = (
        Index("idx_category_slug", slug),  # Búsquedas por slug
        Index("idx_category_parent", parent_id),  # Consultas jerárquicas rápidas
    )