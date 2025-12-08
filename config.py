import streamlit as st
import os

class CadastroDB:
    def __init__(self):

        self.mydb = st.connection(dialect = "postfresql"
  host = os.environ['PGHOST'],
  port = os.environ['PGPORT'],
  database = os.environ['PGDATABASE'],
  username = os.environ['PGUSER'], 
  password = os.environ['PGPASSWORD'])

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
