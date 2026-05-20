import os
from tabulate import tabulate

class ConsoleView:
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def render_menu():
        print("=" * 55)
        print("  📰  HỆ THỐNG TIN TỨC TỰ ĐỘNG - NEWS AGGREGATOR   ")
        print("=" * 55)
        print(" [1] 📂 Quản lý nguồn tin (Sources)")
        print(" [2] 📰 Xem danh sách bài viết (Articles + Phân trang)")
        print(" [3] ⏰ Trình điều khiển & Cấu hình Cronjob")
        print(" [0] 🚪 Thoát chương trình")
        print("-" * 55)

    @staticmethod
    def render_sources_menu():
        print("\n--- 📂 QUẢN LÝ NGUỒN TIN ---")
        print(" 1. Xem danh sách nguồn tin")
        print(" 2. Thêm nguồn tin mới")
        print(" 3. Sửa thông tin nguồn tin")
        print(" 4. Xóa nguồn tin")
        print(" 0. Quay lại menu chính")

    @staticmethod
    def render_cron_menu(is_running):
        status_text = "🟢 ĐANG BẬT" if is_running else "🔴 ĐANG TẮT"
        print(f"\n--- ⏰ ĐIỀU KHIỂN CRONJOB (Trạng thái: {status_text}) ---")
        print(" 1. Kích hoạt Cronjob tự động (Chạy ngầm Threading)")
        print(" 2. Dừng Cronjob tự động")
        print(" 3. Chạy thủ công: Cronjob 1 (Quét lấy Link bài viết)")
        print(" 4. Chạy thủ công: Cronjob 2 (Cập nhật Chi tiết nội dung)")
        print(" 0. Quay lại menu chính")

    @staticmethod
    def print_table(data, headers):
        if not data:
            print("\n 📭 Không có dữ liệu để hiển thị.")
            return
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

    @staticmethod
    def print_message(msg, success=True):
        prefix = "✅" if success else "❌"
        print(f"\n{prefix} {msg}")