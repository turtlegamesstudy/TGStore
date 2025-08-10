from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import sqlite3
import hashlib

app = FastAPI()

# CORS para permitir conexión desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Reemplaza con tu dominio en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para registro/login
class UsuarioRegistro(BaseModel):
    nombre: str
    email: EmailStr
    password: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

# Función para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# Crear tabla si no existe
with get_db_connection() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)
    conn.commit()

# Función para hashear contraseñas
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Endpoint para registrar usuario
@app.post("/registro")
def registrar_usuario(usuario: UsuarioRegistro):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificar si el email ya existe
    existente = cursor.execute("SELECT * FROM usuarios WHERE email = ?", (usuario.email,)).fetchone()
    if existente:
        conn.close()
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # Insertar nuevo usuario con contraseña hasheada
    hashed_pw = hash_password(usuario.password)
    cursor.execute(
        "INSERT INTO usuarios (nombre, email, password) VALUES (?, ?, ?)",
        (usuario.nombre, usuario.email, hashed_pw)
    )
    conn.commit()
    conn.close()
    return {"mensaje": "Usuario registrado exitosamente"}

# Endpoint para login
@app.post("/login")
def login_usuario(usuario: UsuarioLogin):
    conn = get_db_connection()
    cursor = conn.cursor()

    hashed_pw = hash_password(usuario.password)
    resultado = cursor.execute(
        "SELECT * FROM usuarios WHERE email = ? AND password = ?",
        (usuario.email, hashed_pw)
    ).fetchone()
    conn.close()

    if resultado:
        return {"mensaje": "Login exitoso", "usuario": dict(resultado)}
    else:
        raise HTTPException(status_code=401, detail="Credenciales inválidas"}
