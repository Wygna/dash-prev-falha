import os
import streamlit as st

class CadastroDB:
    def __init__(self):

        # Conexão com PostgreSQL usando Streamlit
        self.mydb = st.connection(
            "mydb",
            type="sql",
            url=(
                f"postgresql://{os.environ['PGUSER']}:{os.environ['PGPASSWORD']}"
                f"@{os.environ['PGHOST']}:{os.environ['PGPORT']}/{os.environ['PGDATABASE']}"
            )
        )

        # Obtém um cursor (SQLAlchemy)
        self.cursor = self.mydb.cursor()

        # Criar tabela se não existir
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT,
                password TEXT
            )
        """)

        self.mydb.commit()


# Instância global
db = CadastroDB()
