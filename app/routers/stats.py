from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.problem import Problem

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/")
def get_stats(db: Session = Depends(get_db)):
    total = db.query(func.count(Problem.id)).scalar()
    solved = db.query(func.count(Problem.id)).filter(Problem.solved == True).scalar()

    by_difficulty = (
        db.query(Problem.difficulty, func.count(Problem.id))
        .group_by(Problem.difficulty)
        .all()
    )

    by_topic = (
        db.query(Problem.topic, func.count(Problem.id))
        .group_by(Problem.topic)
        .order_by(func.count(Problem.id).desc())
        .all()
    )

    reviewed_at_least_once = (
        db.query(func.count(Problem.id))
        .filter(Problem.times_reviewed > 0)
        .scalar()
    )

    return {
        "total_problems": total,
        "solved": solved,
        "unsolved": total - solved,
        "reviewed_at_least_once": reviewed_at_least_once,
        "never_reviewed": total - reviewed_at_least_once,
        "by_difficulty": {d: c for d, c in by_difficulty},
        "by_topic": {t: c for t, c in by_topic},
    }
