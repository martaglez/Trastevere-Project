from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_premium = Column(Boolean, default=False)
    stars = Column(Float, nullable=False, server_default="0")
    signup_date = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    publications = relationship("Publication", back_populates="author", cascade="all, delete-orphan")
    collections = relationship("Collection", back_populates="owner", cascade="all, delete-orphan")
    search_history_entries = relationship(
        "SearchHistory", back_populates="user", cascade="all, delete-orphan"
    )
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    following = relationship(
        "Follow",
        foreign_keys="Follow.follower_id",
        back_populates="follower",
        cascade="all, delete-orphan",
    )
    followers = relationship(
        "Follow",
        foreign_keys="Follow.following_id",
        back_populates="following",
        cascade="all, delete-orphan",
    )
    # Añadidas las nuevas características ~Hugo
    dni = Column(String, unique=True, nullable=True)
    phone_number = Column(String, nullable=True)
    card_number = Column(Integer, nullable=True)
    profile_pic = Column(String, nullable=True)


class Publication(Base):
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    image_meta = Column(JSONB, nullable=True)
    save_counter = Column(Integer, nullable=False, server_default="0")

    author = relationship("User", back_populates="publications")
    collection_items = relationship(
        "CollectionItem", back_populates="publication", cascade="all, delete-orphan"
    )
    likes = relationship("Like", back_populates="publication", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")


class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String, nullable=False)

    owner = relationship("User", back_populates="collections")
    items = relationship("CollectionItem", back_populates="collection", cascade="all, delete-orphan")


class CollectionItem(Base):
    __tablename__ = "collection_items"
    __table_args__ = (UniqueConstraint("collection_id", "publication_id", name="uq_collection_publication"),)

    id = Column(Integer, primary_key=True, index=True)
    collection_id = Column(
        Integer, ForeignKey("collections.id", ondelete="CASCADE"), nullable=False, index=True
    )
    publication_id = Column(
        Integer, ForeignKey("publications.id", ondelete="CASCADE"), nullable=False, index=True
    )

    collection = relationship("Collection", back_populates="items")
    publication = relationship("Publication", back_populates="collection_items")


class Like(Base):
    __tablename__ = "likes"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    publication_id = Column(
        Integer, ForeignKey("publications.id", ondelete="CASCADE"), primary_key=True
    )
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user = relationship("User", back_populates="likes")
    publication = relationship("Publication", back_populates="likes")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("publications.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=True, index=True)

    post = relationship("Publication", back_populates="comments")
    user = relationship("User", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], back_populates="replies")
    replies = relationship("Comment", back_populates="parent", cascade="all, delete-orphan")


class Follow(Base):
    __tablename__ = "follows"
    __table_args__ = (CheckConstraint("follower_id <> following_id", name="ck_follows_not_self"),)

    follower_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    following_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    following = relationship("User", foreign_keys=[following_id], back_populates="followers")


class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    query = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user = relationship("User", back_populates="search_history_entries")
