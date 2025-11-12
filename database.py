# database.py
import sqlite3
from datetime import date

DB_NAME = "agenda.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS appuntamenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titolo TEXT NOT NULL,
            descrizione TEXT,
            data TEXT NOT NULL,
            ora TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def aggiungi_appuntamento(titolo, descrizione, data, ora):
    conn = sqlite3.connect(DB_NAME)
    conn.execute('''
        INSERT INTO appuntamenti (titolo, descrizione, data, ora)
        VALUES (?, ?, ?, ?)
    ''', (titolo, descrizione, data, ora))
    conn.commit()
    conn.close()

def get_appuntamenti_giorno(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT titolo, descrizione, ora FROM appuntamenti
        WHERE data = ?
        ORDER BY ora
    ''', (data,))
    risultati = [{'titolo': r[0], 'descrizione': r[1], 'ora': r[2]} for r in cursor.fetchall()]
    conn.close()
    return risultati

def get_appuntamenti_settimana(data_inizio, data_fine):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT titolo, descrizione, data, ora FROM appuntamenti
        WHERE data BETWEEN ? AND ?
        ORDER BY data, ora
    ''', (str(data_inizio), str(data_fine)))
    risultati = [{'titolo': r[0], 'descrizione': r[1], 'data': r[2], 'ora': r[3]} for r in cursor.fetchall()]
    conn.close()
    return risultati