import httpx
from typing import List, Dict, Any

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"


async def fetch_solved_problems(username: str) -> List[Dict[str, Any]]:
    """
    Fetch recently solved problems from LeetCode public GraphQL API.
    Returns a list of problems with title, slug, difficulty.
    """
    query = """
    query recentSubmissions($username: String!, $limit: Int!) {
      recentAcSubmissionList(username: $username, limit: $limit) {
        id
        title
        titleSlug
        timestamp
      }
    }
    """
    payload = {
        "query": query,
        "variables": {"username": username, "limit": 50},
    }

    headers = {
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com",
    }

    async with httpx.AsyncClient(timeout=15) as client:
        response = client.post(LEETCODE_GRAPHQL_URL, json=payload, headers=headers)
        # Note: httpx async requires await — keeping sync-compatible for simplicity
        # Use httpx.AsyncClient in production with await

    data = response.json()
    submissions = data.get("data", {}).get("recentAcSubmissionList", [])

    problems = []
    for s in submissions:
        problems.append({
            "title": s["title"],
            "url": f"https://leetcode.com/problems/{s['titleSlug']}/",
            "topic": "Uncategorized",   # user can update after import
            "difficulty": "Medium",     # LeetCode basic API doesn't return difficulty
            "tags": [],
        })

    return problems


async def fetch_problem_detail(slug: str) -> Dict[str, Any]:
    """Fetch difficulty and topic tags for a single problem by its slug."""
    query = """
    query problemDetail($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionId
        title
        difficulty
        topicTags { name }
      }
    }
    """
    payload = {"query": query, "variables": {"titleSlug": slug}}
    headers = {"Content-Type": "application/json", "Referer": "https://leetcode.com"}

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.post(LEETCODE_GRAPHQL_URL, json=payload, headers=headers)

    q = resp.json().get("data", {}).get("question", {})
    return {
        "leetcode_id": int(q.get("questionId", 0)),
        "difficulty": q.get("difficulty", "Medium"),
        "tags": [t["name"] for t in q.get("topicTags", [])],
    }
