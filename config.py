import streamlit as st
from sqlalchemy import text

class CadastroDB:
    def __init__(self):
        # Conecta ao PostgreSQL usando o secrets.toml
        self.conn = st.connection("mydb", type="sql")

    def criar_tabela(self):
        query = text("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT,
                password TEXT
            )
        """)
        with self.conn.session as s:
            s.execute(query)
            s.commit()

    def inserir(self, name, password):
        query = text("""
            INSERT INTO users (name, password)
            VALUES (:name, :password)
        """)
        with self.conn.session as s:
            s.execute(query, {"name": name, "password": password})
            s.commit()

    def listar(self):
        return self.conn.query("SELECT * FROM users;")
        

# Instância global
db = CadastroDB()
db.criar_tabela()
