from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List

router = APIRouter()

class LeaderboardEntry(BaseModel):
    username: str = Field(..., description="Player username")
    score: int = Field(..., description="Player's score")

# PUBLIC_INTERFACE
@router.get("/", response_model=List[LeaderboardEntry], summary="Get leaderboard", description="Get the current leaderboard standings (stubbed data)")
def get_leaderboard():
    """Stub: returns placeholder leaderboard. Replace with DB-backed logic."""
    return [
        LeaderboardEntry(username="champion1", score=100),
        LeaderboardEntry(username="contender2", score=70)
    ]
