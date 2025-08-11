from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

# Permitir que el frontend (GitHub Pages) se conecte
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://turtlegamesstudy.github.io"],  # dominio de GitHub Pages
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

@app.get("/usuarios")
def obtener_usuarios():
    conn = get_db_connection()
    usuarios = conn.execute("SELECT * FROM usuarios").fetchall()
    conn.close()
    return [dict(row) for row in usuarios]

@app.post("/usuarios")
def agregar_usuario(nombre: str, email: str):
    conn = get_db_connection()
    conn.execute("INSERT INTO usuarios (nombre, email) VALUES (?, ?)", (nombre, email))
    conn.commit()
    conn.close()
    return {"mensaje": "Usuario agregado"}

