from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

# Dummy in-memory representation for game sessions/lobbies (replace with DB)
lobbies = {}
games = {}

router = APIRouter()

# PUBLIC_INTERFACE
class LobbyCreateRequest(BaseModel):
    host_id: str = Field(..., description="Host user id")
    max_players: int = Field(..., description="Max number of players in the lobby")

# PUBLIC_INTERFACE
class Lobby(BaseModel):
    lobby_id: str
    host_id: str
    players: List[str]
    max_players: int

# PUBLIC_INTERFACE
@router.post("/lobby/create", response_model=Lobby, summary="Create a new game lobby")
def create_lobby(req: LobbyCreateRequest):
    """Creates a new lobby for the buckshot roulette game."""
    lobby_id = f"lobby_{len(lobbies)+1}"
    lobbies[lobby_id] = {
        "lobby_id": lobby_id,
        "host_id": req.host_id,
        "players": [req.host_id],
        "max_players": req.max_players,
    }
    return lobbies[lobby_id]

# PUBLIC_INTERFACE
@router.post("/lobby/{lobby_id}/join", response_model=Lobby, summary="Join a lobby by id")
def join_lobby(lobby_id: str, user_id: str):
    """Allows a user to join a lobby if there's space."""
    if lobby_id not in lobbies:
        raise HTTPException(status_code=404, detail="Lobby not found")
    lobby = lobbies[lobby_id]
    if len(lobby["players"]) >= lobby["max_players"]:
        raise HTTPException(status_code=400, detail="Lobby full")
    if user_id not in lobby["players"]:
        lobby["players"].append(user_id)
    return lobby

# PUBLIC_INTERFACE
@router.post("/lobby/{lobby_id}/start", summary="Start a game in a lobby")
def start_game(lobby_id: str):
    """Initializes a buckshot roulette game in specified lobby."""
    if lobby_id not in lobbies:
        raise HTTPException(status_code=404, detail="Lobby not found")
    # Placeholder: implement full game logic/transition to active game state
    games[lobby_id] = {"state": "started", "players": lobbies[lobby_id]["players"]}
    return {"status": "started", "players": games[lobby_id]["players"]}

# PUBLIC_INTERFACE
@router.get("/lobby/{lobby_id}", response_model=Lobby, summary="Get lobby state")
def get_lobby(lobby_id: str):
    """Fetch details of a lobby."""
    if lobby_id not in lobbies:
        raise HTTPException(status_code=404, detail="Lobby not found")
    return lobbies[lobby_id]
