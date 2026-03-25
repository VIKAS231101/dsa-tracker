from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime


class ProblemCreate(BaseModel):
    title: str
    leetcode_id: Optional[int] = None
    url: Optional[str] = None
    topic: str
    difficulty: str                  # Easy | Medium | Hard
    approach: Optional[str] = None
    tags: Optional[List[str]] = []
    solved: Optional[bool] = True


class ProblemUpdate(BaseModel):
    title: Optional[str] = None
    topic: Optional[str] = None
    difficulty: Optional[str] = None
    approach: Optional[str] = None
    tags: Optional[List[str]] = None
    solved: Optional[bool] = None


class ProblemOut(BaseModel):
    id: int
    title: str
    leetcode_id: Optional[int]
    url: Optional[str]
    topic: str
    difficulty: str
    approach: Optional[str]
    tags: List[str]
    solved: bool
    times_reviewed: int
    last_reviewed_at: Optional[datetime]
    next_review_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class ProblemFilter(BaseModel):
    topic: Optional[str] = None
    difficulty: Optional[str] = None
    tags: Optional[List[str]] = None
    solved: Optional[bool] = None
