-- 데이터베이스 생성 (이미 docker-compose에서 생성되지만 확실히 하기 위해)
CREATE DATABASE IF NOT EXISTS fastapi_db;
USE fastapi_db;

-- 사용자 테이블 생성
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 샘플 데이터 삽입
INSERT INTO users (username, email, hashed_password) VALUES
    ('testuser', 'test@example.com', 'password_hashed'),
    ('admin', 'admin@example.com', 'admin_password_hashed');