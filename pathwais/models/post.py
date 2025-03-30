from datetime import datetime
from enum import Enum
from slugify import slugify 
from sqlalchemy import ForeignKey, String, Text, Enum as SQLEnum, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.ext.hybrid import hybrid_property
from .auth import User
from .category import Category
from .comments import BaseComment
from config.extensions import db
import re
from sqlalchemy.sql import func
import os 



class PostStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"

class PostType(str, Enum):
    ARTICLE = "article"
    VIDEO = "video"
    GALLERY = "gallery"

class Post(db.Model):
    __tablename__ = "posts"
    __table_args__ = (
        Index("idx_post_slug", "slug", unique=True),
        Index("idx_post_author_status", "author_id", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    slug: Mapped[str] = mapped_column(String(130), unique=True, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Multimedia (Firebase Storage URLs)
    featured_image: Mapped[str] = mapped_column(String(200), nullable=True)
    media_gallery: Mapped[list[str]] = mapped_column(JSON, default=list)
    
    # Metadata
    status: Mapped[PostStatus] = mapped_column(SQLEnum(PostStatus), default=PostStatus.DRAFT)
    location: Mapped[tuple] = mapped_column(JSON, default=())
    post_type: Mapped[PostType] = mapped_column(SQLEnum(PostType), default=PostType.ARTICLE)
    metadata: Mapped[dict] = mapped_column(JSON, default={
        "seo_title": None,
        "seo_description": None,
        "reading_time": None
    })
    
    # Auditoría
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.utcnow)
    published_at: Mapped[datetime] = mapped_column(nullable=True)
    is_approved: Mapped[bool] = mapped_column(default=False) 
    
    # Relaciones
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
    
    categories: Mapped[list["Category"]] = relationship(
        secondary="post_categories",
        back_populates="posts"
    )
    
    comments: Mapped[list["Comment"]] = relationship(
        primaryjoin="and_(Comment.object_type=='post', Comment.object_id==Post.id)",
        foreign_keys="[Comment.object_id]",
        overlaps="parent,replies",
        viewonly=True
    )
    
    # ---------------------
    # Validaciones
    # ---------------------
    @validates("title")
    def validate_title(self, key, title):
        if len(title) < 10 or len(title) > 120:
            raise ValueError("El título debe tener entre 10 y 120 caracteres")
        return title.strip()

    @validates("slug")
    def validate_slug(self, key, slug):
        if not re.match(r"^[a-z0-9\-]+$", slug):
            raise ValueError("Slug inválido: solo minúsculas, números y guiones")
        return slug


    @hybrid_property
    def comment_count(self):
        return len(self.comments)

    @hybrid_property
    def reading_time(self):
        """Calcula tiempo de lectura estimado (200 palabras/minuto)"""
        words = len(self.content.split())
        return max(1, round(words / 200))

    def publish(self):
        if self.status == PostStatus.PUBLISHED:
            return
        self.status = PostStatus.PUBLISHED
        self.published_at = func.now()

    # ---------------------
    # Firebase Integration
    # ---------------------
    def upload_featured_image(self, file_path: str):
        bucket = storage.bucket()
        blob = bucket.blob(f"posts/{self.id}/featured/{os.path.basename(file_path)}")
        blob.upload_from_filename(file_path)
        self.featured_image = blob.public_url

    def generate_slug(self):
        base_slug = slugify(self.title)
        counter = 1
        new_slug = base_slug
        while Post.query.filter_by(slug=new_slug).first() is not None:
            new_slug = f"{base_slug}-{counter}"
            counter += 1
        self.slug = new_slug