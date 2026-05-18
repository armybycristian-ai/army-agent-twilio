import sqlite3
import logging

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, db_path: str = "army_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY,
                phone_number TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def add_message(self, phone_number: str, role: str, content: str):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute(
                "INSERT INTO conversations (phone_number, role, content) VALUES (?, ?, ?)",
                (phone_number, role, content)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error saving: {str(e)}")

    def get_history(self, phone_number: str, limit: int = 20) -> list:
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                "SELECT role, content FROM conversations WHERE phone_number = ? ORDER BY id DESC LIMIT ?",
                (phone_number, limit)
            ).fetchall()
            conn.close()
            return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]
        except Exception as e:
            logger.error(f"Error retrieving: {str(e)}")
            return []
