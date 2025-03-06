import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st

CONNECTION_STRING = "postgresql://neondb_owner:npg_YqBVZNepQ18x@ep-orange-bread-a9efjwmt-pooler.gwc.azure.neon.tech/neondb?sslmode=require"

def get_connection():
    try:
        conn = psycopg2.connect(CONNECTION_STRING, cursor_factory=RealDictCursor)
        return conn
    except Exception as e:
        st.error("Error connecting to the database.")
        raise e

def run_query(query, params=None):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(query, params)
        try:
            results = cur.fetchall()
        except psycopg2.ProgrammingError:
            results = None
    conn.commit()
    conn.close()
    return results

def execute_query(query, params=None):
    conn = get_connection()
    with conn.cursor() as cur:
        cur.execute(query, params)
    conn.commit()
    conn.close()
