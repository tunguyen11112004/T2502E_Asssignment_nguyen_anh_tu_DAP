from models.SourceModel import SourceModel
from models.CategoryModel import CategoryModel
from views.ConsoleView import ConsoleView

class SourceController:
    @classmethod
    def handle_crud(cls):
        while True:
            ConsoleView.render_sources_menu()
            choice = input("👉 Chọn chức năng (0-4): ").strip()
            
            if choice == '1':
                cls.list_sources()
            elif choice == '2':
                cls.add_source()
            elif choice == '3':
                cls.edit_source()
            elif choice == '4':
                cls.delete_source()
            elif choice == '0':
                break
            else:
                ConsoleView.print_message("Lựa chọn không hợp lệ!", False)

    @classmethod
    def list_sources(cls):
        sources = SourceModel.get_all()
        table_data = [[s['id'], s['source_name'], s['url'], s['category_name']] for s in sources]
        ConsoleView.print_table(table_data, ["ID", "Tên Nguồn", "URL", "Danh Mục"])

    @classmethod
    def add_source(cls):
        name = input("Nhập tên nguồn tin (VD: VnExpress Thể Thao): ").strip()
        url = input("Nhập URL chuyên mục: ").strip()
        
        categories = CategoryModel.get_all()
        print("\n--- Danh sách danh mục hợp lệ ---")
        for cat in categories:
            print(f" [{cat['id']}] {cat['name']}")
            
        try:
            cat_id = int(input("👉 Chọn ID danh mục: "))
            if not any(c['id'] == cat_id for c in categories):
                raise ValueError()
            SourceModel.create(name, url, cat_id)
            ConsoleView.print_message("Thêm nguồn tin mới thành công!")
        except ValueError:
            ConsoleView.print_message("ID danh mục nhập vào không hợp lệ!", False)

    @classmethod
    def edit_source(cls):
        cls.list_sources()
        try:
            source_id = int(input("Nhập ID nguồn cần sửa: "))
            name = input("Nhập tên mới: ").strip()
            url = input("Nhập URL mới: ").strip()
            
            categories = CategoryModel.get_all()
            cat_id = int(input("Chọn ID danh mục mới: "))
            
            SourceModel.update(source_id, name, url, cat_id)
            ConsoleView.print_message("Cập nhật thông tin nguồn tin thành công!")
        except Exception:
            ConsoleView.print_message("Đầu vào sai định dạng. Thất bại!", False)

    @classmethod
    def delete_source(cls):
        cls.list_sources()
        try:
            source_id = int(input("Nhập ID nguồn cần xóa: "))
            SourceModel.delete(source_id)
            ConsoleView.print_message("Xóa nguồn tin thành công!")
        except Exception:
            ConsoleView.print_message("Thao tác thất bại, kiểm tra lại ID!", False)