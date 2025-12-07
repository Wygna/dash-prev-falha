import streamlit as st

class CadastroDB:
    def __init__(self):
        # Conecta usando o bloco [connections.mydb] do secrets.toml
        self.mydb = st.connection("mydb", type="sql")

    def criar_tabela(self):
        self.mydb.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT,
                password TEXT
            )
        """)

    def inserir(self, name, password):
        self.mydb.execute(
            "INSERT INTO users (name, password) VALUES (%s, %s)",
            (name, password)
        )

    def listar(self):
        return self.mydb.query("SELECT * FROM users")
