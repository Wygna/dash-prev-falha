import streamlit as st
import os

class CadastroDB:
    def __init__(self):

        self.mydb = st.connection("mydb", type="sql",
            dialect="postgresql",
            host = os.getenv('PGHOST'),
            port = os.getenv('PGPORT'),
            database = os.getenv('PGDATABASE'),
            username = os.getenv('PGUSER'), 
            password = os.getenv('PGPASSWORD')
        )

        self.cursor = self.mydb.cursor()

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
