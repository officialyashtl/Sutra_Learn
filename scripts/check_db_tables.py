import sys
import sqlite3
sys.path.insert(0, 'backend')
from app.db.database import get_db_path, get_db_connection

p = get_db_path()
print("Resolved DB path:", p)
conn = sqlite3.connect(p)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [r[0] for r in cur.fetchall()]
print("Tables in DB:", tables)

