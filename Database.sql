CREATE DATABASE IF NOT EXISTS news_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE news_management;

-- 1. Bảng danh mục
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

-- 2. Bảng nguồn tin
CREATE TABLE IF NOT EXISTS sources (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_name VARCHAR(100) NOT NULL,
    url VARCHAR(255) NOT NULL,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 3. Bảng bài viết
CREATE TABLE IF NOT EXISTS articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source_id INT,
    category_id INT,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL UNIQUE,
    summary TEXT,
    content TEXT,
    status TINYINT DEFAULT 0, -- 0: Mới lấy link, 1: Đã lấy nội dung
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_id) REFERENCES sources(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- Seed dữ liệu danh mục mẫu
INSERT IGNORE INTO categories (id, name) VALUES 
(1, 'Công nghệ'),
(2, 'Kinh doanh'),
(3, 'Thể thao'),
(4, 'Giải trí'),
(5, 'Sức khỏe');