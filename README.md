# DSA Problem Tracker

A FastAPI + PostgreSQL + Docker app to log, categorize, tag, and revise your DSA problems using spaced repetition.

---

## Features
- Log & categorize problems by topic, difficulty, and approach
- Tagging & smart filter system
- Spaced repetition revision reminders (1 → 3 → 7 → 14 → 30 → 60 day intervals)
- Stats dashboard (by topic, difficulty, review status)
- Import recent accepted submissions from LeetCode

---

## Folder Structure

```
dsa-tracker/
├── app/
│   ├── main.py               # FastAPI entrypoint
│   ├── config.py             # Settings from .env
│   ├── database.py           # SQLAlchemy engine & session
│   ├── models/
│   │   └── problem.py        # Problem DB model
│   ├── schemas/
│   │   └── problem.py        # Pydantic request/response schemas
│   ├── routers/
│   │   ├── problems.py       # CRUD + filter endpoints
│   │   ├── stats.py          # Stats dashboard endpoint
│   │   ├── revision.py       # Spaced repetition endpoints
│   │   └── leetcode_import.py# LeetCode import endpoint
│   └── services/
│       ├── revision.py       # Spaced repetition logic
│       └── leetcode.py       # LeetCode GraphQL API client
├── alembic/                  # DB migrations
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

## Quickstart

### 1. Clone & configure
```bash
git clone <your-repo>
cd dsa-tracker
cp .env.example .env
# Edit .env — add your LeetCode username
```

### 2. Run with Docker
```bash
docker-compose up --build
```

API runs at: http://localhost:8000
Swagger docs: http://localhost:8000/docs

---

## API Endpoints

### Problems
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /problems/ | Add a new problem |
| GET | /problems/ | List all (filter by topic, difficulty, tag, solved) |
| GET | /problems/{id} | Get single problem |
| PUT | /problems/{id} | Update problem |
| DELETE | /problems/{id} | Delete problem |

### Revision
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /revision/due | Problems due for revision today |
| GET | /revision/never-reviewed | Problems never revised |
| POST | /revision/{id}/mark-reviewed | Mark as reviewed, advance interval |

### Stats
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /stats/ | Full dashboard (totals, by topic, by difficulty) |

### Import
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /import/leetcode | Import recent accepted submissions from LeetCode |

---

## Spaced Repetition Schedule
After each review, the next review is scheduled as:

| Review # | Next review in |
|----------|---------------|
| 1st | 1 day |
| 2nd | 3 days |
| 3rd | 7 days |
| 4th | 14 days |
| 5th | 30 days |
| 6th+ | 60 days |

---

## Example: Add a Problem
```bash
curl -X POST http://localhost:8000/problems/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Two Sum",
    "leetcode_id": 1,
    "url": "https://leetcode.com/problems/two-sum/",
    "topic": "Arrays",
    "difficulty": "Easy",
    "approach": "Use a hashmap to store seen values",
    "tags": ["hashmap", "two-pointer"]
  }'
```
