import streamlit as st

class CadastroDB:
    def __init__(self):
        self.mydb = st.connection("mydb", type="sql")

        # Criar tabela se não existir
        with self.mydb.session as session:
            session.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT,
                    password TEXT
                )
            """)
            session.commit()

    def add_user(self, name, password):
        with self.mydb.session as session:
            session.execute("""
                INSERT INTO users (name, password)
                VALUES (:name, :password)
            """, {"name": name, "password": password})
            session.commit()

    def get_users(self):
        return self.mydb.query("SELECT * FROM users")

# Instância global
db = CadastroDB()
