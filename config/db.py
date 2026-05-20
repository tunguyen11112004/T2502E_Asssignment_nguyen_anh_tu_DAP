import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='news_management',
            user='root',       # Điều chỉnh theo cấu hình máy bạn
            password=''        # Điều chỉnh theo cấu hình máy bạn
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"❌ Lỗi kết nối DB: {e}")
        return None