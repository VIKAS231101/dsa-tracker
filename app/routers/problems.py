from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.database import get_db
from app.models.problem import Problem
from app.schemas.problem import ProblemCreate, ProblemUpdate, ProblemOut

router = APIRouter(prefix="/problems", tags=["Problems"])


@router.post("/", response_model=ProblemOut, status_code=201)
def create_problem(problem: ProblemCreate, db: Session = Depends(get_db)):
    db_problem = Problem(**problem.model_dump())
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem


@router.get("/", response_model=List[ProblemOut])
def list_problems(
    topic: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    solved: Optional[bool] = Query(None),
    search: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    q = db.query(Problem)

    if topic:
        q = q.filter(Problem.topic.ilike(f"%{topic}%"))
    if difficulty:
        q = q.filter(Problem.difficulty == difficulty)
    if tag:
        q = q.filter(Problem.tags.any(tag))
    if solved is not None:
        q = q.filter(Problem.solved == solved)
    if search:
        q = q.filter(Problem.title.ilike(f"%{search}%"))

    return q.offset(skip).limit(limit).all()


@router.get("/{problem_id}", response_model=ProblemOut)
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem


@router.put("/{problem_id}", response_model=ProblemOut)
def update_problem(problem_id: int, updates: ProblemUpdate, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(problem, field, value)

    db.commit()
    db.refresh(problem)
    return problem


@router.delete("/{problem_id}", status_code=204)
def delete_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    db.delete(problem)
    db.commit()
