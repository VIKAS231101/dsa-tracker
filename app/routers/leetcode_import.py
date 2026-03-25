from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.problem import Problem
from app.schemas.problem import ProblemOut
from app.services.leetcode import fetch_solved_problems, fetch_problem_detail
from app.config import settings

router = APIRouter(prefix="/import", tags=["Import"])


@router.post("/leetcode", response_model=List[ProblemOut])
async def import_from_leetcode(
    username: str = None,
    db: Session = Depends(get_db)
):
    """
    Import recent accepted submissions from LeetCode.
    Uses LEETCODE_USERNAME from .env if no username passed.
    Skips problems already in DB (matched by URL).
    """
    target = username or settings.LEETCODE_USERNAME
    if not target:
        raise HTTPException(status_code=400, detail="No LeetCode username provided.")

    try:
        problems = await fetch_solved_problems(target)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LeetCode API error: {str(e)}")

    imported = []
    for p in problems:
        existing = db.query(Problem).filter(Problem.url == p["url"]).first()
        if existing:
            continue

        # Try to enrich with difficulty and tags
        slug = p["url"].rstrip("/").split("/")[-1]
        try:
            detail = await fetch_problem_detail(slug)
            p.update(detail)
        except Exception:
            pass  # fall back to defaults if enrichment fails

        db_problem = Problem(**p)
        db.add(db_problem)
        imported.append(db_problem)

    db.commit()
    for prob in imported:
        db.refresh(prob)

    return imported
