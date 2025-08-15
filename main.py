from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Permitir conexión desde tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://turtlegamesstudy.github.io"],  # tu dominio de GitHub Pages
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
            email TEXT NOT NULL
        )
    """)
    conn.commit()

# Modelo de usuario para recibir datos en JSON
class Usuario(BaseModel):
    nombre: str
    email: str

@app.get("/usuarios")
def obtener_usuarios():
    conn = get_db_connection()
    usuarios = conn.execute("SELECT * FROM usuarios").fetchall()
    conn.close()
    return [dict(row) for row in usuarios]

@app.post("/usuarios")
def agregar_usuario(usuario: Usuario):
    conn = get_db_connection()
    conn.execute("INSERT INTO usuarios (nombre, email) VALUES (?, ?)", (usuario.nombre, usuario.email))
    conn.commit()
    conn.close()
    return {"mensaje": "Usuario agregado correctamente"}
