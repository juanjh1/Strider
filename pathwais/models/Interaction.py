from datetime import datetime, timedelta
from config.extensions import db  
from enum import Enum
from sqlalchemy import CheckConstraint, ForeignKey, String, Text, Enum as SQLEnum, Index, JSON
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
from .auth import User

class InteractionType(str, Enum):
    LIKE = "like"
    SAVE = "save"
    SHARE = "share"
    VIEW = "view"
    CLICK = "click"
    FOLLOW = "follow"
    REPORT = "report"
    RATING = "rating"

class UserInteraction(db.Model):
    __tablename__ = "user_interactions"
    __table_args__ = (
        Index("idx_interaction_target", "object_type", "object_id"),
        Index("idx_interaction_user", "user_id", "interaction_type"),
        CheckConstraint(
            "object_type IN ('post', 'product', 'user', 'comment', 'category')",
            name="check_interaction_object_type"
        )
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    object_type: Mapped[str] = mapped_column(String(20))  
    object_id: Mapped[int] = mapped_column()              
    
    interaction_type: Mapped[InteractionType] = mapped_column(
        SQLEnum(InteractionType, name="interaction_type"),
        nullable=False
    )

    metadata: Mapped[dict] = mapped_column(JSON, default={})
    
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="interactions")

    # ---------------------
    # Validaciones
    # ---------------------
    @validates("interaction_type")
    def validate_interaction_type(self, key, value):
        allowed = [t.value for t in InteractionType]
        if value not in allowed:
            raise ValueError(f"Tipo de interacción inválida. Permitidas: {allowed}")
        return value

    @validates("metadata")
    def validate_metadata(self, key, metadata):
        if self.interaction_type == InteractionType.RATING:
            if "value" not in metadata or not (1 <= metadata["value"] <= 5):
                raise ValueError("El rating debe ser entre 1 y 5")
        return metadata

    # ---------------------
    # Métodos útiles
    # ---------------------
    @hybrid_property
    def target(self):
        """Devuelve el objeto relacionado usando el object_type y object_id"""

        if self.object_type == "post":
            return db.session.get(Post, self.object_id)

    @classmethod
    def get_user_activity(cls, user_id: int, days: int = 7):
        """Obtiene las interacciones recientes de un usuario"""
        cutoff_date = func.now() - timedelta(days=days)
        return cls.query.filter(
            cls.user_id == user_id,
            cls.created_at >= cutoff_date
        ).all()