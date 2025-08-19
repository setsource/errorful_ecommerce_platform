
# services/user-service/models.py
import sqlite3
import logging

logger = logging.getLogger(__name__)

class UserModel:
    def __init__(self):
        # Intentional bug: database path doesn't exist
        self.db_path = '/nonexistent/path/users.db'
    
    def get_user(self, user_id):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            conn.close()
            return result
        except Exception as e:
            logger.error(f"Database error: {str(e)}")
            raise

