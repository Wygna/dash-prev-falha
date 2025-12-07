import psycopg2
import streamlit as st


class CadastroDB:
    def __init__(self):
        # Conexão com PostgreSQL usando st.secrets
        self.mydb = psycopg2.connect(
            host=st.secrets["postgres"]["host"],
            user=st.secrets["postgres"]["user"],
            password=st.secrets["postgres"]["password"],
            dbname=st.secrets["postgres"]["database"],
            port=st.secrets["postgres"]["port"]
        )

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


# Instância global para reaproveitar
db = CadastroDB()
