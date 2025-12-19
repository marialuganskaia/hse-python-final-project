from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import declarative_base

from ...domain.models import EventType, UserRole

Base = declarative_base()


class UserORM(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True, default="")
    first_name = Column(String(255), default="")
    last_name = Column(String(255), default="")
    role = Column(Enum(UserRole), nullable=False)
    current_hackathon_id = Column(Integer, ForeignKey("hackathons.id"))


class HackathonORM(Base):
    __tablename__ = "hackathons"
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)


class EventORM(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    hackathon_id = Column(Integer, ForeignKey("hackathons.id"), nullable=False)
    title = Column(String(255), nullable=False)
    type = Column(Enum(EventType), nullable=False)
    starts_at = Column(DateTime, nullable=False)
    ends_at = Column(DateTime, nullable=False)
    location = Column(String(255))
    description = Column(Text)


class FAQItemORM(Base):
    __tablename__ = "faq_items"
    id = Column(Integer, primary_key=True)
    hackathon_id = Column(Integer, ForeignKey("hackathons.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)


class RulesORM(Base):
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True)
    hackathon_id = Column(Integer, ForeignKey("hackathons.id"), nullable=False, unique=True)
    content = Column(Text, nullable=False)


class ReminderSubscriptionORM(Base):
    __tablename__ = "reminder_subscriptions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hackathon_id = Column(Integer, ForeignKey("hackathons.id"), nullable=False)
    enabled = Column(Boolean, default=True)
    __table_args__ = (Index("uq_user_hackathon", "user_id", "hackathon_id", unique=True),)
