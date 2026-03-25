from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ARRAY
from sqlalchemy.sql import func
from app.database import Base


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    leetcode_id = Column(Integer, unique=True, nullable=True)
    url = Column(String(500), nullable=True)

    # Categorization
    topic = Column(String(100), nullable=False)        # e.g. Arrays, Trees, DP
    difficulty = Column(String(10), nullable=False)    # Easy / Medium / Hard
    approach = Column(Text, nullable=True)             # personal notes on approach
    tags = Column(ARRAY(String), default=[])           # e.g. ["sliding-window", "two-pointer"]

    # Status
    solved = Column(Boolean, default=True)
    times_reviewed = Column(Integer, default=0)

    # Spaced repetition
    last_reviewed_at = Column(DateTime(timezone=True), nullable=True)
    next_review_at = Column(DateTime(timezone=True), nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
