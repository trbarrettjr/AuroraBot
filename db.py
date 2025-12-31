#!/usr/bin/python3
import sqlite3

DB_PATH = "aurora.db"

def connect():


def db_insert():
    pass

def db_cleanup():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
                DELETE FROM kp_index
                WHERE timestamp NOT IN (
                    SELECT timestamp
                    FROM kp_index
                    ORDER BY timestamp DESC
                    LIMIT 5760);
                """)
    
    conn.commit()
    conn.close()