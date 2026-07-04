import sqlite3 #transforms schema to database
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "learning_tool.db")

def initialise_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS Reflections (
                Reflection_id        INTEGER  PRIMARY KEY AUTOINCREMENT,
                Given_prompt         TEXT     NOT NULL,
                Reflection_Writing   TEXT     NOT NULL,
                Date                 TEXT     NOT NULL,
                Source_Author        TEXT,
                Media                TEXT     NOT NULL,
                Topic_of_discussion  TEXT,
                Abstract_topic       TEXT,
                Character_referenced TEXT
            )
        """)
        conn.commit()


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_character_name(character_name):
    with get_connection() as conn:
        rows=conn.execute(

            " SELECT * FROM Reflections WHERE Character_referenced = ?",(character_name,)
        ).fetchall()
        return rows


def delete_reflection(character_name,reflection_id):
    with get_connection() as conn:
            conn.execute(

                "DELETE  FROM Reflections WHERE Character_referenced=? AND Reflection_id=?",(character_name,reflection_id,)
               
            )
            conn.commit()

def get_all_character(): #gets all characters
    with get_connection() as conn:
        rows=conn.execute(

            "SELECT Character_referenced FROM Reflections GROUP BY Character_referenced"
        ).fetchall()
        return rows


        
def init_db():
    with get_connection() as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.commit()
    initialise_db()


