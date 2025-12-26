
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .config import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True)

    # Relationship to chat history
    chats = relationship("ChatHistory", back_populates="user")

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    routed_to = Column(String(20), nullable=False)  # "AI" or "Human"
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Foreign key to User
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="chats")