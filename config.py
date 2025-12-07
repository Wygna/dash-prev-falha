import streamlit as st

class CadastroDB:
    def __init__(self):
        # Conecta ao PostgreSQL usando o secrets.toml
        self.conn = st.connection("mydb", type="sql")

    def criar_tabela(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT,
                password TEXT
            )
        """)

    def inserir(self, name, password):
        self.conn.execute(
            "INSERT INTO users (name, password) VALUES (%s, %s)",
            (name, password)
        )

    def listar(self):
        return self.conn.query("SELECT * FROM users")
        

# ===== INSTANCIAR AQUI =====
db = CadastroDB()
db.criar_tabela()
