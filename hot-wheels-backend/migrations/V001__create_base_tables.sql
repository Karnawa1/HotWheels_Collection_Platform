-- ============================================
-- V001: Create Base Tables
-- Hot Wheels Platform Database Schema
-- ============================================

\echo '📦 V001: Creating base tables...'

-- 1. НЕЗАВИСИМЫЕ ТАБЛИЦЫ

-- Производители
CREATE TABLE IF NOT EXISTS manufacturers (
    manufacturer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(50),
    founded_year INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Пользователи
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(150),
    country VARCHAR(50),
    city VARCHAR(100),
    profile_image_url TEXT,
    bio TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    role VARCHAR(20) DEFAULT 'collector' CHECK (role IN ('collector', 'trader', 'admin', 'moderator')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    CONSTRAINT email_format CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

\echo '  ✓ Base tables (manufacturers, users) created'

-- 2. ТАБЛИЦЫ ПЕРВОГО УРОВНЯ

-- Серии
CREATE TABLE IF NOT EXISTS series (
    series_id SERIAL PRIMARY KEY,
    series_name VARCHAR(150) NOT NULL,
    release_year INT NOT NULL,
    manufacturer_id INT REFERENCES manufacturers(manufacturer_id),
    description TEXT,
    is_limited_edition BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_series_year UNIQUE(series_name, release_year)
);

-- Кастинги
CREATE TABLE IF NOT EXISTS castings (
    casting_id SERIAL PRIMARY KEY,
    casting_name VARCHAR(200) NOT NULL,
    first_release_year INT NOT NULL,
    manufacturer_id INT REFERENCES manufacturers(manufacturer_id),
    scale VARCHAR(10) DEFAULT '1:64',
    designer VARCHAR(100),
    based_on_real_car BOOLEAN DEFAULT FALSE,
    real_car_model VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_year CHECK (first_release_year >= 1968)
);

-- Сессии пользователей
CREATE TABLE IF NOT EXISTS user_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    ip_address INET,
    user_agent TEXT,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_expiry CHECK (expires_at > created_at)
);

\echo '  ✓ First level tables (series, castings, sessions) created'

-- 3. ТАБЛИЦЫ ВТОРОГО УРОВНЯ

-- Конкретные модели
CREATE TABLE IF NOT EXISTS car_models (
    model_id SERIAL PRIMARY KEY,
    casting_id INT NOT NULL REFERENCES castings(casting_id),
    series_id INT REFERENCES series(series_id),
    release_year INT NOT NULL,
    color VARCHAR(50) NOT NULL,
    tampo_design VARCHAR(200),
    wheel_type VARCHAR(100),
    base_color VARCHAR(50),
    window_color VARCHAR(50),
    interior_color VARCHAR(50),
    production_code VARCHAR(10),
    sku VARCHAR(50) UNIQUE,
    rarity_level VARCHAR(20) CHECK (rarity_level IN ('Common', 'Uncommon', 'Rare', 'Chase', 'Super Treasure Hunt')),
    estimated_production_quantity INT,
    msrp NUMERIC(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_model_variation UNIQUE(casting_id, series_id, release_year, color, tampo_design)
);

\echo '  ✓ Second level tables (car_models) created'

-- 4. ТАБЛИЦЫ ТРЕТЬЕГО УРОВНЯ

-- Изображения моделей
CREATE TABLE IF NOT EXISTS model_images (
    image_id SERIAL PRIMARY KEY,
    model_id INT NOT NULL REFERENCES car_models(model_id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    image_type VARCHAR(20) CHECK (image_type IN ('product', 'packaging', 'detail', 'user_photo')),
    is_primary BOOLEAN DEFAULT FALSE,
    uploaded_by INT REFERENCES users(user_id),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Коллекции пользователей
CREATE TABLE IF NOT EXISTS user_collections (
    collection_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    model_id INT NOT NULL REFERENCES car_models(model_id),
    acquisition_date DATE DEFAULT CURRENT_DATE,
    acquisition_price NUMERIC(10,2),
    condition VARCHAR(20) CHECK (condition IN ('Mint', 'Near Mint', 'Excellent', 'Good', 'Fair', 'Poor')),
    is_in_package BOOLEAN DEFAULT TRUE,
    package_condition VARCHAR(20),
    quantity INT DEFAULT 1 CHECK (quantity > 0),
    storage_location VARCHAR(100),
    notes TEXT,
    is_for_trade BOOLEAN DEFAULT FALSE,
    is_for_sale BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_model UNIQUE(user_id, model_id, acquisition_date)
);

-- Wishlist
CREATE TABLE IF NOT EXISTS wishlists (
    wishlist_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    model_id INT NOT NULL REFERENCES car_models(model_id),
    priority INT CHECK (priority BETWEEN 1 AND 5),
    max_price_willing NUMERIC(10,2),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_wishlist_item UNIQUE(user_id, model_id)
);

-- Листинги
CREATE TABLE IF NOT EXISTS listings (
    listing_id SERIAL PRIMARY KEY,
    seller_id INT NOT NULL REFERENCES users(user_id),
    collection_item_id INT REFERENCES user_collections(collection_id),
    model_id INT NOT NULL REFERENCES car_models(model_id),
    listing_type VARCHAR(20) NOT NULL CHECK (listing_type IN ('sale', 'trade', 'auction')),
    price NUMERIC(10,2),
    condition VARCHAR(20) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'sold', 'cancelled', 'expired')),
    views_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    sold_at TIMESTAMP,
    CONSTRAINT check_price_positive CHECK (price IS NULL OR price > 0)
);

\echo '  ✓ Third level tables (images, collections, wishlists, listings) created'

-- 5. ТАБЛИЦЫ ЧЕТВЕРТОГО УРОВНЯ

-- Транзакции
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id SERIAL PRIMARY KEY,
    listing_id INT NOT NULL REFERENCES listings(listing_id),
    buyer_id INT NOT NULL REFERENCES users(user_id),
    seller_id INT NOT NULL REFERENCES users(user_id),
    transaction_type VARCHAR(20) NOT NULL CHECK (transaction_type IN ('purchase', 'trade')),
    amount NUMERIC(10,2) NOT NULL CHECK (amount >= 0),
    payment_method VARCHAR(50),
    payment_status VARCHAR(20) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'completed', 'failed', 'refunded')),
    shipping_status VARCHAR(20) DEFAULT 'not_shipped' CHECK (shipping_status IN ('not_shipped', 'shipped', 'in_transit', 'delivered')),
    tracking_number VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    CONSTRAINT check_different_users CHECK (buyer_id != seller_id)
);

-- Отзывы
CREATE TABLE IF NOT EXISTS reviews (
    review_id SERIAL PRIMARY KEY,
    transaction_id INT NOT NULL REFERENCES transactions(transaction_id),
    reviewer_id INT NOT NULL REFERENCES users(user_id),
    reviewee_id INT NOT NULL REFERENCES users(user_id),
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_transaction_reviewer UNIQUE(transaction_id, reviewer_id)
);

\echo '  ✓ Fourth level tables (transactions, reviews) created'

\echo '✅ V001: All base tables created successfully!'
