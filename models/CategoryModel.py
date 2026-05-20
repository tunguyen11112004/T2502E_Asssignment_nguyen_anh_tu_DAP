from config.Db import get_connection

class CategoryModel:
    @staticmethod
    def get_all():
        conn = get_connection()
        if not conn: return []
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categories")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result