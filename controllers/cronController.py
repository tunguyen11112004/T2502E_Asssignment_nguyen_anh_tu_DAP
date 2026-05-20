import schedule
import time
import threading
from models.SourceModel import SourceModel
from models.ArticleModel import ArticleModel
from services.CrawlerService import CrawlerService
from views.ConsoleView import ConsoleView

class CronController:
    _cron_thread = None
    _stop_event = threading.Event()
    is_running = False

    @classmethod
    def job_fetch_links(cls):
        print("\n🔄 [Cronjob 1] Bắt đầu quét liên kết từ các nguồn...")
        sources = SourceModel.get_all()
        new_links_count = 0
        
        for src in sources:
            found_articles = CrawlerService.fetch_links_from_source(src['url'])
            for art in found_articles:
                inserted = ArticleModel.insert_link_if_not_exists(
                    source_id=src['id'],
                    category_id=src['category_id'],
                    title=art['title'],
                    url=art['url']
                )
                if inserted:
                    new_links_count += 1
        print(f"🌟 [Cronjob 1] Đã hoàn thành quét. Đã nạp thành công {new_links_count} liên kết mới!")

    @classmethod
    def job_update_details(cls):
        print("\n🔄 [Cronjob 2] Bắt đầu lấy chi tiết nội dung các bài viết...")
        pending_list = ArticleModel.get_pending_articles()
        
        # Khởi tạo bộ đếm thống kê
        total_pending = len(pending_list)
        success_count = 0
        failed_count = 0
        
        if total_pending == 0:
            print("🌟 [Cronjob 2] Không có bài viết nào cần cập nhật nội dung.")
            return
            
        for index, art in enumerate(pending_list, start=1):
            print(f"-> Đang xử lý bài {index}/{total_pending}: {art['url'][:50]}...")
            
            try:
                # Tiến hành crawl nội dung
                summary, content = CrawlerService.fetch_article_detail(art['url'])
                
                # Kiểm tra nếu lấy dữ liệu thành công và không bị rỗng
                if summary and content and content != "Không thể bóc tách nội dung chi tiết.":
                    ArticleModel.update_content(art['id'], summary, content)
                    success_count += 1
                else:
                    # Trường hợp kết nối được nhưng cấu hình HTML sai không lấy được text
                    failed_count += 1
                    
            except Exception as e:
                # Bỏ qua khi gặp lỗi kết nối/timeout và cộng vào bộ đếm thất bại
                failed_count += 1
                continue
                
            finally:
                # Tăng thời gian delay lên một chút (2-3 giây) để giảm tần suất gửi request, 
                # giúp né bộ lọc chặn Bot/Crawler của các trang báo lớn.
                time.sleep(2.5) 
                
        # Hiển thị bảng tổng kết kết quả sau khi quét xong toàn bộ danh sách
        print("\n" + "="*50)
        print("📊 TỔNG KẾT TIẾN TRÌNH CẬP NHẬT NỘI DUNG")
        print("="*50)
        print(f" Total (Tổng số bài viết chờ xử lý) : {total_pending}")
        print(f" Success (Cập nhật thành công)     : 🟢 {success_count}")
        print(f" Failed (Bỏ qua do lỗi/Timeout)    : 🔴 {failed_count}")
        print("="*50 + "\n")

    @classmethod
    def _run_schedule(cls):
        while not cls._stop_event.is_set():
            schedule.run_pending()
            time.sleep(1)

    @classmethod
    def handle_cron_menu(cls):
        while True:
            ConsoleView.render_cron_menu(cls.is_running)
            choice = input("👉 Chọn chức năng (0-4): ").strip()
            
            if choice == '1':
                if not cls.is_running:
                    cls._stop_event.clear()
                    schedule.clear()
                    # Cấu hình lịch chạy tự động theo yêu cầu bài toán
                    schedule.every().day.at("08:00").do(cls.job_fetch_links)
                    schedule.every(30).minutes.do(cls.job_update_details)

                    # schedule.every(30).seconds.do(cls.job_fetch_links) #test
                    # schedule.every(30).seconds.do(cls.job_update_details)
                    
                    cls._cron_thread = threading.Thread(target=cls._run_schedule, daemon=True)
                    cls._cron_thread.start()
                    cls.is_running = True
                    ConsoleView.print_message("Kích hoạt vòng lặp Cronjob chạy ngầm thành công!")
                else:
                    ConsoleView.print_message("Hệ thống Cronjob tự động vốn đang chạy rồi.", False)
            
            elif choice == '2':
                if cls.is_running:
                    cls._stop_event.set()
                    schedule.clear()
                    cls.is_running = False
                    ConsoleView.print_message("Đã tắt tiến trình Cronjob chạy ngầm.")
                else:
                    ConsoleView.print_message("Hệ thống hiện tại chưa bật chạy ngầm.", False)
                    
            elif choice == '3':
                cls.job_fetch_links()
            elif choice == '4':
                cls.job_update_details()
            elif choice == '0':
                break