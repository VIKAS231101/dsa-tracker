from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.problem import ProblemOut
from app.services.revision import mark_reviewed, get_due_for_revision, get_never_reviewed

router = APIRouter(prefix="/revision", tags=["Revision"])


@router.get("/due", response_model=List[ProblemOut])
def due_for_revision(db: Session = Depends(get_db)):
    """Get all problems due for revision today based on spaced repetition schedule."""
    return get_due_for_revision(db)


@router.get("/never-reviewed", response_model=List[ProblemOut])
def never_reviewed(db: Session = Depends(get_db)):
    """Get problems that have never been revised."""
    return get_never_reviewed(db)


@router.post("/{problem_id}/mark-reviewed", response_model=ProblemOut)
def mark_problem_reviewed(problem_id: int, db: Session = Depends(get_db)):
    """Mark a problem as reviewed — advances its spaced repetition interval."""
    problem = mark_reviewed(db, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem
