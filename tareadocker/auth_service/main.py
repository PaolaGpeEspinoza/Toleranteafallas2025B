from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import json
import os

app = FastAPI()

SECRET_KEY = os.environ.get("SECRET_KEY", "DEFAULT_KEY")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
USERS_FILE = "users.json"

# ---------------------------
# FUNCIONES PARA EL ARCHIVO
# ---------------------------

def load_users():
    """Carga los usuarios desde users.json"""
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # archivo corrupto -> tratar como vacío
        return {}

def save_users(users: dict):
    """Guarda los usuarios en users.json (escribe atómico)"""
    tmp = USERS_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)
    os.replace(tmp, USERS_FILE)

# ---------------------------
# MODELOS
# ---------------------------

class UserSignup(BaseModel):
    username: str
    password: str

# ---------------------------
# FUNCIONES INTERNAS
# ---------------------------

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

def hash_password(password):
    return pwd_context.hash(password)

def create_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(hours=2)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

# ---------------------------
# ENDPOINTS
# ---------------------------

@app.post("/signup")
def signup(data: UserSignup):
    username = data.username
    password = data.password

    users = load_users()
    if username in users:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    users[username] = hash_password(password)
    save_users(users)
    return {"message": "Usuario registrado correctamente"}

# -------------------------------------------------
# ENDPOINT DE SALUD PARA KUBERNETES (Liveness/Readiness)
# -------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    users = load_users()
    user_hashed = users.get(form_data.username)

    if not user_hashed or not verify_password(form_data.password, user_hashed):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    token = create_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/validate")
def validate(user: dict = Depends(get_current_user)):
    return {"status": "ok", "user": user["sub"]}
