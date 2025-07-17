from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, EmailStr
import hashlib

# Dummy in-memory storage for demonstration (replace with real db ops)
user_db = {}

router = APIRouter()

# PUBLIC_INTERFACE
class UserRegister(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=30, description="Username for display")
    password: str = Field(..., min_length=6, description="Password (min 6 chars)")

# PUBLIC_INTERFACE
class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="Password")

# PUBLIC_INTERFACE
class UserProfile(BaseModel):
    user_id: str = Field(..., description="Unique user ID")
    email: EmailStr
    username: str

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# PUBLIC_INTERFACE
@router.post("/register", response_model=UserProfile, summary="Register new user")
def register_user(user: UserRegister):
    """Registers a new user with email, username, and password."""
    if user.email in user_db:
        raise HTTPException(status_code=409, detail="Email already registered")
    user_id = str(len(user_db) + 1)
    user_db[user.email] = {
        "user_id": user_id,
        "email": user.email,
        "username": user.username,
        "password_hash": hash_password(user.password)
    }
    # In production, perform DB insert here using the game_database connection!
    return UserProfile(user_id=user_id, email=user.email, username=user.username)

# PUBLIC_INTERFACE
@router.post("/login", response_model=UserProfile, summary="User login")
def login_user(login: UserLogin):
    """Authenticate a user and return their profile if successful."""
    user_data = user_db.get(login.email)
    if not user_data or user_data["password_hash"] != hash_password(login.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return UserProfile(
        user_id=user_data["user_id"],
        email=user_data["email"],
        username=user_data["username"]
    )

# PUBLIC_INTERFACE
@router.get("/profile/{user_id}", response_model=UserProfile, summary="Get user profile")
def get_user_profile(user_id: str):
    """Fetch user profile information by user_id."""
    for data in user_db.values():
        if data["user_id"] == user_id:
            return UserProfile(
                user_id=data["user_id"],
                email=data["email"],
                username=data["username"]
            )
    raise HTTPException(status_code=404, detail="User not found")
