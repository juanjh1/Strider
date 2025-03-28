from config.extensions import db  
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from enum import Enum
from datetime import datetime
from sqlalchemy.sql import func
import bcrypt



class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class StatusUser(db.Model):
    __tablename__ = "status_user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True,  nullable=False)
    users: Mapped[list["User"]] = relationship(back_populates="status_info")

class Permission(db.Model):
    __tablename__ = "permission"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    roles: Mapped[list["Role"]] = relationship(
        secondary="role_permission", 
        back_populates="permissions"
    )


class Role(db.Model):
    __tablename__ = "role"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    users: Mapped[list["User"]] = relationship(
        secondary="user_role", 
        back_populates="roles"
    )
    permissions: Mapped[list["Permission"]] = relationship(
        secondary="role_permission", 
        back_populates="roles"
    )



class RolePermission(db.Model):
    __tablename__ = "role_permission"
    permission : Mapped[int] = mapped_column(ForeignKey("permission.id"), primary_key=True)
    role : Mapped[int] = mapped_column(ForeignKey("role.id"), primary_key=True)


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    password : Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] =  mapped_column(unique=True, nullable=False)
    gender: Mapped[Gender] = mapped_column(SQLAlchemyEnum(Gender, native_enum=False), nullable=False)
    created_at:Mapped[datetime] = mapped_column(
                                                DateTime(), 
                                                server_default=func.now()
                                                )
    last_seen: Mapped[datetime] = mapped_column(
                                                DateTime(), 
                                                server_default=func.now()
                                                )
    status_id: Mapped[int] = mapped_column(ForeignKey("status_user.id")) 
    status_info: Mapped["StatusUser"] = relationship(back_populates="users")  
    roles: Mapped[list["Role"]] = relationship(
        secondary="user_role", 
        back_populates="users"
    )

    def set_password(self, password: str):
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password.encode("utf-8"))
    
    def is_admin(self) -> bool:
        return any(role.name == "admin" for role in self.roles)



class UserRole(db.Model):
    __tablename__ = "user_role"
    user : Mapped[int] = mapped_column(ForeignKey("user.id"),  primary_key=True)
    role : Mapped[int] = mapped_column(ForeignKey("role.id"),  primary_key=True)



