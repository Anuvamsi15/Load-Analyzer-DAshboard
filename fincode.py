import streamlit as st
import pandas as pd
import re
import sqlite3
import plotly.express as px
from datetime import datetime

# --- DATABASE LOGIC (Manual Schema) ---
def create_db_schema():
    """Manually defines the SQL table structure"""
    conn = sqlite3.connect('hpc_logs.db')
    cursor = conn.cursor()
    # Define your schema manually here
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS structured_logs (
            LineId INTEGER PRIMARY KEY,
            Node TEXT,
            Component TEXT,
            State TEXT,
            Time REAL,
            Content TEXT,
            Detected_IP TEXT,
            Timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

def save_to_sqlite(df):
    """Saves the processed dataframe to the manually created table"""
    create_db_schema() # Ensure table exists first
    conn = sqlite3.connect('hpc_logs.db')
    
    # We use if_exists='replace' now because the table is manually created.
    # To keep it fresh like your original code, we clear it first.
    
    # Save data
    df.to_sql('structured_logs', conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()

conn = sqlite3.connect('hpc_logs.db')
conn.row_factory = sqlite3.Row

rows = conn.execute("SELECT LineId, Node FROM structured_logs").fetchall()

for row in rows:
    print(f"{row['LineId']:<6} | {row['Node']:<20}")

conn.close()

    

