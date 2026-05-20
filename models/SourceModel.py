from config.Db import get_connection

class SourceModel:
    @staticmethod
    def create(source_name, url, category_id):
        conn = get_connection()
        if not conn: return
        cursor = conn.cursor()
        query = "INSERT INTO sources (source_name, url, category_id) VALUES (%s, %s, %s)"
        cursor.execute(query, (source_name, url, category_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        if not conn: return []
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT s.*, c.name as category_name 
            FROM sources s 
            LEFT JOIN categories c ON s.category_id = c.id
        """
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def update(source_id, source_name, url, category_id):
        conn = get_connection()
        if not conn: return
        cursor = conn.cursor()
        query = "UPDATE sources SET source_name=%s, url=%s, category_id=%s WHERE id=%s"
        cursor.execute(query, (source_name, url, category_id, source_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete(source_id):
        conn = get_connection()
        if not conn: return
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sources WHERE id = %s", (source_id,))
        conn.commit()
        cursor.close()
        conn.close()