from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.models.problem import Problem


# Spaced repetition intervals in days: review 1, 3, 7, 14, 30, 60
INTERVALS = [1, 3, 7, 14, 30, 60]


def get_next_interval(times_reviewed: int) -> int:
    idx = min(times_reviewed, len(INTERVALS) - 1)
    return INTERVALS[idx]


def mark_reviewed(db: Session, problem_id: int) -> Problem:
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        return None

    now = datetime.now(timezone.utc)
    days = get_next_interval(problem.times_reviewed)

    problem.times_reviewed += 1
    problem.last_reviewed_at = now
    problem.next_review_at = now + timedelta(days=days)

    db.commit()
    db.refresh(problem)
    return problem


def get_due_for_revision(db: Session) -> list[Problem]:
    now = datetime.now(timezone.utc)
    return (
        db.query(Problem)
        .filter(Problem.next_review_at <= now)
        .order_by(Problem.next_review_at)
        .all()
    )


def get_never_reviewed(db: Session) -> list[Problem]:
    return (
        db.query(Problem)
        .filter(Problem.last_reviewed_at == None)
        .order_by(Problem.created_at)
        .all()
    )
