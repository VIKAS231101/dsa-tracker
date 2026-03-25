from fastapi import FastAPI
from app.database import Base, engine
from app.routers import problems, stats, revision
from app.routers import leetcode_import

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DSA Problem Tracker",
    description="Track, categorize, tag, and revise your DSA problems with spaced repetition.",
    version="1.0.0",
)

# Register routers
app.include_router(problems.router)
app.include_router(stats.router)
app.include_router(revision.router)
app.include_router(leetcode_import.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "DSA Tracker API is running"}
