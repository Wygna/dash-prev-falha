import sqlite3
import streamlit as st

class CadastroDB:
    def __init__(self, db_name="cadastro.db"):
        self.mydb = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.mydb.cursor()

        # Criar tabela se não existir
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            password TEXT
        )
        """)
        self.mydb.commit()

# Instância global para reaproveitar
db = CadastroDB()