from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from . import user, game, ws, leaderboard

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="Buckshot Roulette VR API",
    version="1.0.0",
    description="Backend service for multiplayer buckshot roulette VR game. Provides authentication, matchmaking, real-time communication, and core game logic."
)

# CORS setup for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint.
    Returns 200 OK if the service is running.
    """
    return {"message": "Healthy"}

# --- AUTH and USER ENDPOINTS ---

app.include_router(user.router, prefix="/user", tags=["User"])

# --- GAME ENDPOINTS ---
app.include_router(game.router, prefix="/game", tags=["Game"])

# --- LEADERBOARD (stub) ---
app.include_router(leaderboard.router, prefix="/leaderboard", tags=["Leaderboard"])

# --- WEBSOCKET ENTRIES ---
ws.register_ws_routes(app)

# --- EXTERNAL API INTEGRATION STUB ---

@app.get("/external/thirdparty", tags=["External"], summary="External API integration stub", description="Demonstrates where 3rd party integrations would be implemented.")
def external_api_stub():
    """Stub endpoint for demonstrating integration with external services (e.g., payment, analytics)."""
    return {"message": "Third-party integration point. Implement as needed."}

# --- USAGE DOCS FOR WEBSOCKET ---
@app.get("/ws/info", tags=["WebSocket"], summary="WebSocket Usage", description="How to connect to WebSocket endpoints.")
def websocket_info():
    """Returns documentation on WebSocket usage for frontend clients."""
    return {
        "ws_url": "/ws/game",
        "description": "Connect via WebSocket for lobby, chat, and real-time game events. Send/receive JSON.",
        "handlers": [
            "/ws/game - Lobby and game events",
            "/ws/chat - Global/chatroom events"
        ]
    }
