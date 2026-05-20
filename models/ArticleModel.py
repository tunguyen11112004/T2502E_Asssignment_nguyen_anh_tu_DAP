from config.Db import get_connection

class ArticleModel:
    @staticmethod
    def insert_link_if_not_exists(source_id, category_id, title, url):
        conn = get_connection()
        if not conn: return False
        cursor = conn.cursor()
        query = """
            INSERT IGNORE INTO articles (source_id, category_id, title, url, status) 
            VALUES (%s, %s, %s, %s, 0)
        """
        cursor.execute(query, (source_id, category_id, title, url))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        return affected > 0

    @staticmethod
    def get_pending_articles():
        conn = get_connection()
        if not conn: return []
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, url FROM articles WHERE status = 0")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def update_content(article_id, summary, content):
        conn = get_connection()
        if not conn: return
        cursor = conn.cursor()
        query = "UPDATE articles SET summary=%s, content=%s, status=1 WHERE id=%s"
        cursor.execute(query, (summary, content, article_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def get_paginated(limit, offset):
        conn = get_connection()
        if not conn: return []
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT a.id, a.title, a.url, c.name as category_name, a.status 
            FROM articles a
            LEFT JOIN categories c ON a.category_id = c.id
            ORDER BY a.created_at DESC LIMIT %s OFFSET %s
        """
        cursor.execute(query, (limit, offset))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def count_all():
        conn = get_connection()
        if not conn: return 0
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM articles")
        result = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return result