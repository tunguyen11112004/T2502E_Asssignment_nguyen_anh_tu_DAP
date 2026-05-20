from models.ArticleModel import ArticleModel
from views.ConsoleView import ConsoleView

class ArticleController:
    @staticmethod
    def list_articles_with_pagination():
        limit = 10
        current_page = 1
        
        while True:
            total_articles = ArticleModel.count_all()
            total_pages = (total_articles + limit - 1) // limit
            if total_pages == 0: total_pages = 1
            
            offset = (current_page - 1) * limit
            articles = ArticleModel.get_paginated(limit, offset)
            
            ConsoleView.clear_screen()
            print(f"\n📰 --- DANH SÁCH BÀI VIẾT (Trang {current_page}/{total_pages}) ---")
            
            table_data = []
            for a in articles:
                status_str = "🟢 Đầy đủ" if a['status'] == 1 else "⚪ Chỉ có Link"
                short_title = a['title'][:45] + "..." if len(a['title']) > 45 else a['title']
                table_data.append([a['id'], short_title, a['category_name'], status_str])
                
            ConsoleView.print_table(table_data, ["ID", "Tiêu đề ngắn", "Danh mục", "Trạng thái"])
            
            print("\n 👉 [N] Trang sau | [P] Trang trước | [0] Quay lại Menu")
            action = input("Nhập lệnh: ").strip().upper()
            
            if action == 'N' and current_page < total_pages:
                current_page += 1
            elif action == 'P' and current_page > 1:
                current_page -= 1
            elif action == '0':
                break