import streamlit as st
from sqlalchemy import text

class CadastroDB:
    def __init__(self):
        self.mydb = st.connection("mydb", type="sql")

        # Criar tabela se não existir
        with self.mydb.session as session:
            session.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT,
                    password TEXT
                )
            """))
            session.commit()

    def add_user(self, name, password):
        with self.mydb.session as session:
            session.execute(text("""
                INSERT INTO users (name, password)
                VALUES (:name, :password)
            """), {"name": name, "password": password})
            session.commit()

    def get_users(self):
        return self.mydb.query("SELECT * FROM users")

db = CadastroDB()
