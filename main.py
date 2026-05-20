from views.ConsoleView import ConsoleView
from controllers.SourceController import SourceController
from controllers.ArticleController import ArticleController
from controllers.CronController import CronController

def main():
    while True:
        ConsoleView.render_menu()
        choice = input("👉 Mời nhập lựa chọn của bạn (0-3): ").strip()
        
        if choice == '1':
            SourceController.handle_crud()
        elif choice == '2':
            ArticleController.list_articles_with_pagination()
        elif choice == '3':
            CronController.handle_cron_menu()
        elif choice == '0':
            if CronController.is_running:
                CronController._stop_event.set()
            ConsoleView.print_message("Hệ thống đóng an toàn. Tạm biệt!")
            break
        else:
            ConsoleView.print_message("Lựa chọn không hợp lệ, vui lòng thử lại!", False)

if __name__ == "__main__":
    main()