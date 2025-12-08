import streamlit as st
import psycopg2
import os

class CadastroDB:
    def __init__(self):

        self.mydb = psycopg2.connect(
            host = os.getenv('PGHOST'),
            port = os.getenv('PGPORT'),
            database = os.getenv('PGDATABASE'),
            user = os.getenv('PGUSER'), 
            password = os.getenv('PGPASSWORD')
        )

        self.cursor = self.mydb.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT,
            password TEXT
        )
        """)

        self.mydb.commit()

# Instância global para reaproveitar
db = CadastroDB()
