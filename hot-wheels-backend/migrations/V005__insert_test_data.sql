-- ============================================
-- V005: Insert Test Data
-- Sample data for development and testing
-- ============================================

\echo '🌱 V005: Inserting test data...'

DO $$ 
BEGIN
    -- Отключаем проверку FK для очистки
    SET session_replication_role = 'replica';
    
    -- Удаляем данные в обратном порядке зависимостей
    TRUNCATE TABLE reviews CASCADE;
    TRUNCATE TABLE transactions CASCADE;
    TRUNCATE TABLE listings CASCADE;
    TRUNCATE TABLE wishlists CASCADE;
    TRUNCATE TABLE user_collections CASCADE;
    TRUNCATE TABLE model_images CASCADE;
    TRUNCATE TABLE user_sessions CASCADE;
    TRUNCATE TABLE car_models CASCADE;
    TRUNCATE TABLE castings CASCADE;
    TRUNCATE TABLE series CASCADE;
    TRUNCATE TABLE users CASCADE;
    TRUNCATE TABLE manufacturers CASCADE;
    
    -- Включаем обратно проверку FK
    SET session_replication_role = 'origin';
    
    RAISE NOTICE 'Tables truncated successfully';
END $$;

-- Сброс sequences
ALTER SEQUENCE manufacturers_manufacturer_id_seq RESTART WITH 1;
ALTER SEQUENCE series_series_id_seq RESTART WITH 1;
ALTER SEQUENCE castings_casting_id_seq RESTART WITH 1;
ALTER SEQUENCE car_models_model_id_seq RESTART WITH 1;
ALTER SEQUENCE users_user_id_seq RESTART WITH 1;
ALTER SEQUENCE user_collections_collection_id_seq RESTART WITH 1;
ALTER SEQUENCE wishlists_wishlist_id_seq RESTART WITH 1;
ALTER SEQUENCE listings_listing_id_seq RESTART WITH 1;
ALTER SEQUENCE transactions_transaction_id_seq RESTART WITH 1;
ALTER SEQUENCE reviews_review_id_seq RESTART WITH 1;
ALTER SEQUENCE model_images_image_id_seq RESTART WITH 1;
-- ============================================
-- 1. ПРОИЗВОДИТЕЛИ
-- ============================================

INSERT INTO manufacturers (name, country, founded_year) VALUES
('Mattel', 'USA', 1945),
('Matchbox', 'UK', 1953),
('Tomica', 'Japan', 1970),
('Majorette', 'France', 1964);

-- ============================================
-- 2. СЕРИИ (ИСПРАВЛЕНО - уникальные названия)
-- ============================================

INSERT INTO series (series_name, release_year, manufacturer_id, description, is_limited_edition) VALUES
-- Mattel серии
('Mainline', 2025, 1, 'Basic assortment cars', FALSE),
('Mainline', 2024, 1, 'Basic assortment cars', FALSE),
('Mainline', 2023, 1, 'Basic assortment cars', FALSE),
('Treasure Hunt', 2025, 1, 'Special treasure hunt series', TRUE),
('Treasure Hunt', 2024, 1, 'Special treasure hunt series', TRUE),
('Super Treasure Hunt', 2025, 1, 'Ultra rare chase cars with Spectraflame paint', TRUE),
('Super Treasure Hunt', 2024, 1, 'Ultra rare chase cars with Spectraflame paint', TRUE),
('Car Culture', 2025, 1, 'Premium adult collector series', TRUE),
('Car Culture', 2024, 1, 'Premium adult collector series', TRUE),
('Fast & Furious', 2025, 1, 'Movie-themed cars', TRUE),
('Red Line Club', 2025, 1, 'Exclusive RLC member cars', TRUE),
('Red Line Club', 2024, 1, 'Exclusive RLC member cars', TRUE),
('HW Premium', 2025, 1, 'Metal body and real riders', TRUE),
('Team Transport', 2025, 1, 'Car and truck sets', TRUE),
('Boulevard', 2024, 1, 'JDM and Euro cars', TRUE),
-- Matchbox серии
('MBX Mainline', 2025, 2, 'Matchbox main line', FALSE),
('MBX Moving Parts', 2025, 2, 'Cars with working features', TRUE),
-- Tomica серии
('Tomica Regular', 2025, 3, 'Standard Tomica line', FALSE),
('Tomica Premium', 2025, 3, 'Premium detailed models', TRUE);

-- ============================================
-- 3. КАСТИНГИ (базовые модели)
-- ============================================

INSERT INTO castings (casting_name, first_release_year, manufacturer_id, scale, designer, based_on_real_car, real_car_model) VALUES
-- Classic Hot Wheels
('Custom ''67 Pontiac Firebird', 1968, 1, '1:64', 'Ira Gilford', TRUE, 'Pontiac Firebird 1967'),
('Custom Mustang', 1968, 1, '1:64', 'Howard Rees', TRUE, 'Ford Mustang 1965'),
('Custom Camaro', 1968, 1, '1:64', 'Ira Gilford', TRUE, 'Chevrolet Camaro 1968'),
('Bone Shaker', 2006, 1, '1:64', 'Larry Wood', FALSE, NULL),
('Deora II', 2000, 1, '1:64', 'Chip Foose', FALSE, NULL),

-- Modern sports cars
('Nissan Skyline GT-R (R34)', 2001, 1, '1:64', 'Phil Riehlman', TRUE, 'Nissan Skyline GT-R R34'),
('Toyota Supra', 1998, 1, '1:64', 'Phil Riehlman', TRUE, 'Toyota Supra MK4'),
('Mazda RX-7', 1995, 1, '1:64', 'Phil Riehlman', TRUE, 'Mazda RX-7 FD'),
('Honda Civic Type R', 2019, 1, '1:64', 'Brendon Vetuskey', TRUE, 'Honda Civic Type R FK8'),
('Lamborghini Aventador', 2012, 1, '1:64', 'Fraser Campbell', TRUE, 'Lamborghini Aventador LP700-4'),

-- American muscle
('''69 Dodge Charger', 1970, 1, '1:64', 'Larry Wood', TRUE, 'Dodge Charger 1969'),
('Plymouth Barracuda', 1970, 1, '1:64', 'Larry Wood', TRUE, 'Plymouth Barracuda 1970'),
('''70 Chevelle SS', 1970, 1, '1:64', 'Larry Wood', TRUE, 'Chevrolet Chevelle SS 1970'),
('Ford GT-40', 1970, 1, '1:64', 'Mark Jones', TRUE, 'Ford GT40'),
('Shelby GT500', 2007, 1, '1:64', 'Phil Riehlman', TRUE, 'Shelby GT500'),

-- Trucks and vans
('Custom ''77 Dodge Van', 1977, 1, '1:64', 'George Trosley', TRUE, 'Dodge Van 1977'),
('Ford F-150', 1999, 1, '1:64', 'Phil Riehlman', TRUE, 'Ford F-150'),
('Tesla Cybertruck', 2020, 1, '1:64', 'Brendon Vetuskey', TRUE, 'Tesla Cybertruck'),

-- Fantasy cars
('Twin Mill', 1969, 1, '1:64', 'Ira Gilford', FALSE, NULL),
('Jet Threat', 1971, 1, '1:64', 'Larry Wood', FALSE, NULL),
('Rodger Dodger', 1974, 1, '1:64', 'Larry Wood', FALSE, NULL);

-- ============================================
-- 4. МОДЕЛИ (конкретные вариации)
-- ============================================

INSERT INTO car_models (casting_id, series_id, release_year, color, tampo_design, wheel_type, base_color, window_color, interior_color, production_code, sku, rarity_level, estimated_production_quantity, msrp) VALUES

-- 2025 Mainline (series_id = 1)
(6, 1, 2025, 'Blue', 'Racing stripes', '5-Spoke', 'Black', 'Clear', 'Black', 'A10', 'HW2025-001', 'Common', 500000, 1.25),
(7, 1, 2025, 'Red', 'Fast & Furious graphics', 'Deep Dish', 'Chrome', 'Clear', 'Black', 'A10', 'HW2025-002', 'Common', 500000, 1.25),
(8, 1, 2025, 'Orange', 'Flame decals', 'Racing', 'Black', 'Clear', 'Tan', 'A10', 'HW2025-003', 'Common', 500000, 1.25),
(9, 1, 2025, 'Yellow', 'Type R graphics', 'Y5', 'Black', 'Clear', 'Black', 'A10', 'HW2025-004', 'Common', 500000, 1.25),
(10, 1, 2025, 'Orange', 'Aventador tampo', 'MC5', 'Black', 'Clear', 'Black', 'A10', 'HW2025-005', 'Common', 500000, 1.25),

-- 2024 Mainline (series_id = 2)
(6, 2, 2024, 'Silver', 'GT-R tampo', '5-Spoke', 'Black', 'Clear', 'Black', 'B23', 'HW2024-045', 'Common', 500000, 1.25),
(7, 2, 2024, 'White', 'TRD graphics', 'Real Riders', 'Chrome', 'Clear', 'Red', 'B23', 'HW2024-046', 'Uncommon', 200000, 1.25),
(11, 2, 2024, 'Black', 'Charger R/T tampo', 'Redline', 'Chrome', 'Clear', 'Black', 'B23', 'HW2024-047', 'Common', 500000, 1.25),

-- 2025 Treasure Hunt (series_id = 4)
(4, 4, 2025, 'Green', 'TH logo flame', 'Real Riders', 'Gold', 'Clear', 'Black', 'A15', 'HW2025-TH01', 'Rare', 50000, 1.25),
(19, 4, 2025, 'Purple', 'TH Twin Mill', 'Real Riders', 'Chrome', 'Clear', NULL, 'A15', 'HW2025-TH02', 'Rare', 50000, 1.25),

-- 2025 Super Treasure Hunt (series_id = 6)
(6, 6, 2025, 'Blue Spectraflame', 'STH GT-R logo', 'Real Riders Gold', 'Chrome', 'Clear', 'Black', 'A20', 'HW2025-STH01', 'Super Treasure Hunt', 5000, 1.25),
(7, 6, 2025, 'Orange Spectraflame', 'STH Supra', 'Real Riders Gold', 'Chrome', 'Clear', 'Black', 'A20', 'HW2025-STH02', 'Super Treasure Hunt', 5000, 1.25),

-- 2024 Super Treasure Hunt (series_id = 7)
(8, 7, 2024, 'Red Spectraflame', 'STH RX-7', 'Real Riders Gold', 'Chrome', 'Clear', 'Black', 'C18', 'HW2024-STH05', 'Super Treasure Hunt', 5000, 1.25),

-- 2025 Car Culture (series_id = 8) - Premium series
(6, 8, 2025, 'Purple', 'Bayside Blue graphics', 'Real Riders Premium', 'Black', 'Clear', 'Black', 'A25', 'CC2025-01', 'Rare', 30000, 5.99),
(7, 8, 2025, 'White', 'The Fast Saga', 'Real Riders Premium', 'Black', 'Clear', 'Red', 'A25', 'CC2025-02', 'Rare', 30000, 5.99),
(8, 8, 2025, 'Yellow', 'Initial D tribute', 'Real Riders Premium', 'Black', 'Clear', 'Black', 'A25', 'CC2025-03', 'Rare', 30000, 5.99),

-- 2025 Red Line Club (series_id = 11) - Ultra exclusive
(1, 11, 2025, 'Red Spectraflame', 'Original Redline', 'Redline Wheels', 'Chrome', 'Clear', 'White', 'RLC01', 'RLC2025-01', 'Chase', 10000, 25.00),
(2, 11, 2025, 'Blue Spectraflame', 'Custom Mustang RLC', 'Redline Wheels', 'Chrome', 'Clear', 'Black', 'RLC01', 'RLC2025-02', 'Chase', 10000, 25.00),

-- 2024 Red Line Club (series_id = 12)
(3, 12, 2024, 'Orange Spectraflame', 'Camaro SS RLC', 'Redline Wheels', 'Chrome', 'Clear', 'Black', 'RLC24', 'RLC2024-15', 'Chase', 10000, 25.00),

-- 2025 Team Transport (series_id = 14)
(11, 14, 2025, 'Black', 'Mopar graphics', 'Real Riders', 'Chrome', 'Smoke', 'Red', 'TT01', 'TT2025-01', 'Rare', 20000, 12.99),

-- 2024 Boulevard (series_id = 15) - JDM series
(6, 15, 2024, 'White', 'Nismo graphics', 'Real Riders', 'Black', 'Clear', 'Red', 'BD24', 'BD2024-08', 'Rare', 25000, 4.99),
(7, 15, 2024, 'Silver', 'TRD Pro', 'Real Riders', 'Black', 'Clear', 'Black', 'BD24', 'BD2024-09', 'Rare', 25000, 4.99),

-- 2025 HW Premium (series_id = 13)
(15, 13, 2025, 'Black', 'Shelby stripes', 'Real Riders', 'Chrome', 'Clear', 'Red', 'PR01', 'HWPREM2025-01', 'Rare', 35000, 4.99);

-- ============================================
-- 5. ПОЛЬЗОВАТЕЛИ
-- ============================================

INSERT INTO users (username, email, password_hash, full_name, country, city, profile_image_url, bio, is_verified, role) VALUES
('collector_mike', 'mike@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYuZzHCS.Ia', 'Mike Johnson', 'USA', 'Los Angeles', 'https://i.pravatar.cc/150?img=12', 'Hot Wheels collector since 1995. Love JDM cars!', TRUE, 'collector'),
('jdm_hunter', 'john.smith@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYuZzHCS.Ia', 'John Smith', 'USA', 'San Francisco', 'https://i.pravatar.cc/150?img=33', 'JDM enthusiast. Looking for GT-Rs and Supras!', TRUE, 'trader'),
('euro_collector', 'anna.mueller@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYuZzHCS.Ia', 'Anna Mueller', 'Germany', 'Berlin', 'https://i.pravatar.cc/150?img=45', 'European car collector', TRUE, 'collector'),
('muscle_car_fan', 'bob.williams@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYuZzHCS.Ia', 'Bob Williams', 'USA', 'Detroit', 'https://i.pravatar.cc/150?img=56', 'American muscle only! Chargers, Camaros, Mustangs.', TRUE, 'collector'),
('treasure_seeker', 'sarah.lopez@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYuZzHCS.Ia', 'Sarah Lopez', 'Mexico', 'Mexico City', 'https://i.pravatar.cc/150?img=23', 'Treasure Hunt specialist', TRUE, 'trader'),
('rlc_member', 'david.chen@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYuZzHCS.Ia', 'David Chen', 'Canada', 'Toronto', 'https://i.pravatar.cc/150?img=68', 'RLC member since 2010. Premium collector.', TRUE, 'trader'),
('fantasy_lover', 'emma.taylor@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYuZzHCS.Ia', 'Emma Taylor', 'UK', 'London', 'https://i.pravatar.cc/150?img=41', 'I love fantasy castings! Bone Shaker, Twin Mill, Deora II.', TRUE, 'collector'),
('new_collector', 'alex.brown@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYuZzHCS.Ia', 'Alex Brown', 'Australia', 'Sydney', 'https://i.pravatar.cc/150?img=14', 'Just started collecting in 2024', FALSE, 'collector'),
('admin_user', 'admin@hotwheelsplatform.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYuZzHCS.Ia', 'Platform Admin', 'USA', 'New York', NULL, 'Platform administrator', TRUE, 'admin'),
('mod_user', 'moderator@hotwheelsplatform.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYuZzHCS.Ia', 'Platform Moderator', 'USA', 'Chicago', NULL, 'Platform moderator', TRUE, 'moderator'),
('trader_pro', 'carlos.garcia@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYuZzHCS.Ia', 'Carlos Garcia', 'Spain', 'Madrid', 'https://i.pravatar.cc/150?img=51', 'Professional trader. 500+ trades completed.', TRUE, 'trader'),
('vintage_hunter', 'lisa.anderson@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYuZzHCS.Ia', 'Lisa Anderson', 'USA', 'Miami', 'https://i.pravatar.cc/150?img=29', 'Vintage Hot Wheels from 1968-1980', TRUE, 'collector'),
('sth_collector', 'kevin.nguyen@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYuZzHCS.Ia', 'Kevin Nguyen', 'Vietnam', 'Ho Chi Minh', 'https://i.pravatar.cc/150?img=62', 'Super Treasure Hunt collector', TRUE, 'collector'),
('mainline_only', 'jessica.white@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYuZzHCS.Ia', 'Jessica White', 'USA', 'Seattle', 'https://i.pravatar.cc/150?img=38', 'Budget collector - mainline only', TRUE, 'collector'),
('premium_collector', 'robert.jones@email.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYuZzHCS.Ia', 'Robert Jones', 'USA', 'Boston', 'https://i.pravatar.cc/150?img=71', 'Premium lines only. Car Culture, Team Transport, RLC.', TRUE, 'collector');

-- ============================================
-- 6. КОЛЛЕКЦИИ ПОЛЬЗОВАТЕЛЕЙ
-- ============================================

INSERT INTO user_collections (user_id, model_id, acquisition_date, acquisition_price, condition, is_in_package, package_condition, quantity, storage_location, notes, is_for_trade, is_for_sale) VALUES

-- collector_mike (user_id = 1) - JDM focus
(1, 1, '2025-01-15', 1.25, 'Mint', TRUE, 'Mint', 1, 'Display Case A1', 'Found at Target', FALSE, FALSE),
(1, 6, '2024-11-20', 1.25, 'Mint', TRUE, 'Mint', 1, 'Display Case A1', 'My favorite GT-R', FALSE, FALSE),
(1, 11, '2025-01-10', 6.99, 'Mint', TRUE, 'Mint', 1, 'Premium Display', 'Car Culture - awesome detail', FALSE, FALSE),
(1, 12, '2025-01-10', 6.99, 'Mint', TRUE, 'Mint', 1, 'Premium Display', 'Finally got the white Supra!', FALSE, FALSE),
(1, 17, '2024-08-15', 5.99, 'Near Mint', TRUE, 'Excellent', 1, 'Premium Display', 'Boulevard series', FALSE, FALSE),
(1, 7, '2024-12-01', 2.50, 'Mint', TRUE, 'Mint', 2, 'Storage Box 1', 'Duplicate for trade', TRUE, FALSE),

-- jdm_hunter (user_id = 2) - Active trader
(2, 1, '2025-01-20', 1.25, 'Mint', TRUE, 'Mint', 1, 'Display Wall', 'Skyline R34', FALSE, FALSE),
(2, 2, '2025-01-18', 1.50, 'Mint', TRUE, 'Mint', 1, 'Display Wall', 'Fast & Furious edition', FALSE, FALSE),
(2, 9, '2024-12-10', 75.00, 'Mint', TRUE, 'Mint', 1, 'Safe Storage', 'STH GT-R! My grail!', FALSE, FALSE),
(2, 11, '2025-01-05', 7.50, 'Mint', TRUE, 'Mint', 3, 'Trade Box', 'Extras for trading', TRUE, FALSE),
(2, 3, '2024-10-30', 1.25, 'Excellent', FALSE, NULL, 1, 'Loose Display', 'Opened for display', FALSE, FALSE),

-- euro_collector (user_id = 3)
(3, 5, '2025-01-12', 1.25, 'Mint', TRUE, 'Mint', 1, 'Euro Section', 'Lamborghini Aventador', FALSE, FALSE),
(3, 13, '2024-09-20', 6.99, 'Mint', TRUE, 'Mint', 1, 'Premium Wall', 'Car Culture RX-7', FALSE, FALSE),

-- muscle_car_fan (user_id = 4) - American muscle
(4, 8, '2024-11-15', 1.25, 'Mint', TRUE, 'Mint', 1, 'Muscle Display', 'Dodge Charger', FALSE, FALSE),
(4, 16, '2025-01-08', 15.00, 'Mint', TRUE, 'Mint', 1, 'Safe', 'Team Transport Charger', FALSE, FALSE),
(4, 15, '2024-07-20', 28.00, 'Mint', TRUE, 'Mint', 1, 'RLC Vault', 'RLC Camaro', FALSE, FALSE),
(4, 14, '2025-01-25', 25.00, 'Mint', TRUE, 'Mint', 1, 'RLC Vault', 'Just arrived!', FALSE, FALSE),

-- treasure_seeker (user_id = 5) - TH specialist
(5, 7, '2024-12-20', 8.00, 'Mint', TRUE, 'Mint', 1, 'TH Display', 'Regular Treasure Hunt', FALSE, FALSE),
(5, 8, '2025-01-02', 10.00, 'Mint', TRUE, 'Mint', 1, 'TH Display', 'Another TH!', FALSE, FALSE),
(5, 9, '2024-11-30', 95.00, 'Mint', TRUE, 'Mint', 1, 'STH Vault', 'Super Treasure Hunt GT-R', FALSE, FALSE),
(5, 10, '2024-12-15', 85.00, 'Mint', TRUE, 'Mint', 1, 'STH Vault', 'STH Supra', FALSE, FALSE),
(5, 1, '2025-01-10', 1.25, 'Mint', TRUE, 'Mint', 5, 'Trade Stock', 'For trading', TRUE, TRUE),

-- rlc_member (user_id = 6) - Premium only
(6, 14, '2025-01-20', 25.00, 'Mint', TRUE, 'Mint', 1, 'RLC Room', 'RLC Firebird', FALSE, FALSE),
(6, 15, '2024-08-10', 25.00, 'Mint', TRUE, 'Mint', 1, 'RLC Room', 'RLC Camaro', FALSE, FALSE),
(6, 11, '2025-01-15', 6.99, 'Mint', TRUE, 'Mint', 1, 'Premium Shelf', 'Car Culture', FALSE, FALSE),
(6, 12, '2025-01-15', 6.99, 'Mint', TRUE, 'Mint', 1, 'Premium Shelf', 'Car Culture', FALSE, FALSE),
(6, 13, '2024-10-05', 6.99, 'Mint', TRUE, 'Mint', 1, 'Premium Shelf', 'Car Culture', FALSE, FALSE),

-- fantasy_lover (user_id = 7)
(7, 7, '2024-12-25', 9.00, 'Mint', TRUE, 'Mint', 1, 'Fantasy Section', 'TH Bone Shaker', FALSE, FALSE),

-- new_collector (user_id = 8) - Budget collector
(8, 1, '2025-01-28', 1.25, 'Mint', TRUE, 'Mint', 1, 'Shelf', 'My first Hot Wheels!', FALSE, FALSE),
(8, 2, '2025-01-28', 1.25, 'Mint', TRUE, 'Mint', 1, 'Shelf', 'Second purchase', FALSE, FALSE),
(8, 4, '2025-02-01', 1.25, 'Mint', TRUE, 'Mint', 1, 'Shelf', 'Love the yellow color', FALSE, FALSE),

-- trader_pro (user_id = 11)
(11, 1, '2024-09-10', 1.00, 'Mint', TRUE, 'Mint', 10, 'Trade Inventory', 'Bulk purchase for trading', TRUE, TRUE),
(11, 2, '2024-09-10', 1.00, 'Mint', TRUE, 'Mint', 10, 'Trade Inventory', 'Bulk purchase for trading', TRUE, TRUE),
(11, 3, '2024-09-10', 1.00, 'Mint', TRUE, 'Mint', 10, 'Trade Inventory', 'Bulk purchase for trading', TRUE, TRUE),

-- vintage_hunter (user_id = 12) - Vintage only
(12, 14, '2024-06-15', 30.00, 'Mint', TRUE, 'Mint', 1, 'Vintage Vault', 'RLC Redline tribute', FALSE, FALSE),

-- sth_collector (user_id = 13)
(13, 9, '2024-12-05', 100.00, 'Mint', TRUE, 'Mint', 1, 'STH Safe', 'STH Skyline', FALSE, FALSE),
(13, 10, '2024-11-20', 90.00, 'Mint', TRUE, 'Mint', 1, 'STH Safe', 'STH Supra', FALSE, FALSE),
(13, 11, '2024-10-15', 110.00, 'Mint', TRUE, 'Mint', 1, 'STH Safe', 'STH RX-7', FALSE, FALSE),

-- mainline_only (user_id = 14)
(14, 1, '2025-01-05', 1.25, 'Mint', TRUE, 'Mint', 1, 'Shelf 1', 'Budget collecting', FALSE, FALSE),
(14, 2, '2025-01-05', 1.25, 'Mint', TRUE, 'Mint', 1, 'Shelf 1', 'Budget collecting', FALSE, FALSE),
(14, 3, '2025-01-05', 1.25, 'Mint', TRUE, 'Mint', 1, 'Shelf 1', 'Budget collecting', FALSE, FALSE),
(14, 4, '2025-01-10', 1.25, 'Mint', TRUE, 'Mint', 1, 'Shelf 1', 'Budget collecting', FALSE, FALSE),
(14, 5, '2025-01-10', 1.25, 'Mint', TRUE, 'Mint', 1, 'Shelf 1', 'Budget collecting', FALSE, FALSE),

-- premium_collector (user_id = 15)
(15, 11, '2025-01-20', 6.99, 'Mint', TRUE, 'Mint', 1, 'Premium Display 1', 'Car Culture', FALSE, FALSE),
(15, 12, '2025-01-20', 6.99, 'Mint', TRUE, 'Mint', 1, 'Premium Display 1', 'Car Culture', FALSE, FALSE),
(15, 13, '2024-11-10', 6.99, 'Mint', TRUE, 'Mint', 1, 'Premium Display 1', 'Car Culture', FALSE, FALSE),
(15, 16, '2025-01-15', 15.00, 'Mint', TRUE, 'Mint', 1, 'Premium Display 2', 'Team Transport', FALSE, FALSE),
(15, 14, '2025-02-01', 25.00, 'Mint', TRUE, 'Mint', 1, 'RLC Display', 'RLC Firebird', FALSE, FALSE);

-- ============================================
-- 7. WISHLIST
-- ============================================

INSERT INTO wishlists (user_id, model_id, priority, max_price_willing, notes) VALUES
-- collector_mike wants STH cars
(1, 9, 5, 100.00, 'My grail car! Will pay up to $100'),
(1, 10, 5, 95.00, 'Need this STH Supra'),
(1, 13, 4, 120.00, 'STH RX-7 would complete my JDM set'),

-- jdm_hunter
(2, 13, 4, 70.00, 'Need this Car Culture RX-7'),
(2, 17, 3, 60.00, 'Boulevard GT-R'),

-- muscle_car_fan
(4, 14, 5, 30.00, 'Need RLC Firebird'),

-- treasure_seeker
(5, 13, 5, 150.00, 'Will pay premium for this STH'),

-- new_collector - budget wishlist
(8, 6, 3, 2.00, 'Want a GT-R but on budget'),
(8, 7, 3, 2.00, 'Supra would be cool'),
(8, 8, 2, 2.00, 'RX-7 mainline'),

-- mainline_only
(14, 8, 4, 1.50, 'Looking for Charger mainline'),

-- premium_collector
(15, 14, 5, 28.00, 'Need RLC Firebird'),
(15, 15, 5, 28.00, 'RLC Camaro wanted');

-- ============================================
-- 8. ЛИСТИНГИ (marketplace)
-- ============================================

INSERT INTO listings (seller_id, collection_item_id, model_id, listing_type, price, condition, description, status, views_count, created_at, expires_at) VALUES

-- Active listings
(5, NULL, 1, 'sale', 2.50, 'Mint', 'Mainline Skyline GT-R 2025. Mint in package. Fast shipping!', 'active', 45, '2025-02-05 10:00:00', '2025-03-07 10:00:00'),
(5, NULL, 1, 'trade', NULL, 'Mint', 'Trading for STH cars or RLC exclusives', 'active', 23, '2025-02-06 14:30:00', '2025-03-08 14:30:00'),
(11, NULL, 1, 'sale', 1.75, 'Mint', 'Bulk sale - 10 available. Discount on multiple purchases.', 'active', 67, '2025-02-01 08:00:00', '2025-03-03 08:00:00'),
(11, NULL, 2, 'sale', 1.75, 'Mint', 'Fast & Furious Supra mainline. Perfect condition.', 'active', 89, '2025-02-01 08:15:00', '2025-03-03 08:15:00'),
(11, NULL, 3, 'sale', 1.75, 'Mint', 'RX-7 mainline 2025. Great for traders.', 'active', 54, '2025-02-01 08:30:00', '2025-03-03 08:30:00'),
(2, NULL, 11, 'sale', 12.00, 'Mint', 'Car Culture GT-R. Extra copy for sale. Premium details, real riders.', 'active', 112, '2025-02-03 16:00:00', '2025-03-05 16:00:00'),

-- Sold listings
(5, NULL, 7, 'sale', 15.00, 'Mint', 'Treasure Hunt Bone Shaker 2024. Rare find!', 'sold', 156, '2025-01-15 12:00:00', '2025-02-14 12:00:00'),
(13, NULL, 9, 'sale', 120.00, 'Mint', 'Super Treasure Hunt Skyline GT-R. Spectraflame paint, gold real riders.', 'sold', 342, '2024-12-20 09:00:00', '2025-01-19 09:00:00'),
(4, NULL, 15, 'sale', 35.00, 'Mint', 'RLC Camaro 2024. Limited edition.', 'sold', 201, '2024-11-10 11:00:00', '2024-12-10 11:00:00'),

-- Cancelled listing
(2, NULL, 9, 'sale', 150.00, 'Mint', 'Changed my mind, keeping this STH', 'cancelled', 78, '2025-01-25 15:00:00', NULL),

-- Expired listing
(7, NULL, 7, 'trade', NULL, 'Mint', 'Looking to trade TH for other TH cars', 'expired', 34, '2024-12-01 10:00:00', '2025-01-01 10:00:00');

-- ============================================
-- 9. ТРАНЗАКЦИИ
-- ============================================

INSERT INTO transactions (listing_id, buyer_id, seller_id, transaction_type, amount, payment_method, payment_status, shipping_status, tracking_number, created_at, completed_at) VALUES

-- Completed transactions
(7, 3, 5, 'purchase', 15.00, 'PayPal', 'completed', 'delivered', '1Z999AA10123456784', '2025-01-16 14:30:00', '2025-01-23 10:15:00'),
(8, 6, 13, 'purchase', 120.00, 'Credit Card', 'completed', 'delivered', '1Z999AA10123456785', '2024-12-21 10:00:00', '2024-12-28 16:20:00'),
(9, 15, 4, 'purchase', 35.00, 'PayPal', 'completed', 'delivered', '1Z999AA10123456786', '2024-11-11 09:00:00', '2024-11-18 11:30:00'),

-- Pending/In-transit transactions
(1, 2, 5, 'purchase', 2.50, 'PayPal', 'completed', 'in_transit', '1Z999AA10123456787', '2025-02-06 12:00:00', '2025-02-06 12:30:00'),
(4, 14, 11, 'purchase', 1.75, 'Credit Card', 'completed', 'shipped', '1Z999AA10123456788', '2025-02-04 15:00:00', '2025-02-04 15:45:00'),
(5, 8, 11, 'purchase', 1.75, 'PayPal', 'pending', 'not_shipped', NULL, '2025-02-07 18:00:00', NULL);

-- ============================================
-- 10. ОТЗЫВЫ (Reviews)
-- ============================================

INSERT INTO reviews (transaction_id, reviewer_id, reviewee_id, rating, comment, created_at) VALUES

-- Reviews for completed transactions
(1, 3, 5, 5, 'Perfect transaction! Car arrived quickly and exactly as described. Excellent packaging.', '2025-01-24 12:00:00'),
(1, 5, 3, 5, 'Great buyer, fast payment. Smooth transaction!', '2025-01-24 14:00:00'),

(2, 6, 13, 5, 'Amazing STH! Worth every penny. Seller was very professional and shipping was fast.', '2024-12-29 10:00:00'),
(2, 13, 6, 5, 'Excellent buyer, immediate payment. Highly recommended!', '2024-12-29 11:00:00'),

(3, 15, 4, 5, 'RLC Camaro is perfect! Great communication and fast shipping.', '2024-11-19 09:00:00'),
(3, 4, 15, 5, 'Smooth transaction, would sell to again.', '2024-11-19 10:00:00'),

(4, 2, 5, 5, 'Car just arrived, looks great! Thanks!', '2025-02-07 16:00:00');

-- ============================================
-- 11. ИЗОБРАЖЕНИЯ МОДЕЛЕЙ
-- ============================================

INSERT INTO model_images (model_id, image_url, image_type, is_primary, uploaded_by, uploaded_at) VALUES

-- Skyline GT-R images
(1, 'https://images.hotwheels.com/2025/skyline-gtr-r34-blue-front.jpg', 'product', TRUE, 9, '2025-01-10 10:00:00'),
(1, 'https://images.hotwheels.com/2025/skyline-gtr-r34-blue-side.jpg', 'product', FALSE, 9, '2025-01-10 10:01:00'),
(1, 'https://images.hotwheels.com/2025/skyline-gtr-r34-blue-package.jpg', 'packaging', FALSE, 9, '2025-01-10 10:02:00'),
(1, 'https://user-uploads.hotwheels.com/user1-skyline-collection.jpg', 'user_photo', FALSE, 1, '2025-01-16 14:00:00'),

-- Supra images
(2, 'https://images.hotwheels.com/2025/supra-red-front.jpg', 'product', TRUE, 9, '2025-01-10 10:10:00'),
(2, 'https://images.hotwheels.com/2025/supra-red-package.jpg', 'packaging', FALSE, 9, '2025-01-10 10:11:00'),

-- RX-7 images
(3, 'https://images.hotwheels.com/2025/rx7-orange-front.jpg', 'product', TRUE, 9, '2025-01-10 10:20:00'),
(3, 'https://images.hotwheels.com/2025/rx7-orange-detail.jpg', 'detail', FALSE, 9, '2025-01-10 10:21:00'),

-- STH Skyline
(9, 'https://images.hotwheels.com/2025/sth-skyline-spectraflame-front.jpg', 'product', TRUE, 9, '2025-01-15 09:00:00'),
(9, 'https://images.hotwheels.com/2025/sth-skyline-spectraflame-package.jpg', 'packaging', FALSE, 9, '2025-01-15 09:01:00'),
(9, 'https://images.hotwheels.com/2025/sth-skyline-wheels-closeup.jpg', 'detail', FALSE, 9, '2025-01-15 09:02:00'),
(9, 'https://user-uploads.hotwheels.com/user2-sth-skyline-display.jpg', 'user_photo', FALSE, 2, '2024-12-12 18:00:00'),

-- Car Culture GT-R
(11, 'https://images.hotwheels.com/2025/car-culture-gtr-purple-front.jpg', 'product', TRUE, 9, '2025-01-12 11:00:00'),
(11, 'https://images.hotwheels.com/2025/car-culture-gtr-purple-package.jpg', 'packaging', FALSE, 9, '2025-01-12 11:01:00'),

-- RLC Firebird
(14, 'https://images.hotwheels.com/2025/rlc-firebird-red-front.jpg', 'product', TRUE, 9, '2025-01-18 10:00:00'),
(14, 'https://images.hotwheels.com/2025/rlc-firebird-red-side.jpg', 'product', FALSE, 9, '2025-01-18 10:01:00'),
(14, 'https://images.hotwheels.com/2025/rlc-firebird-red-package.jpg', 'packaging', FALSE, 9, '2025-01-18 10:02:00'),
(14, 'https://images.hotwheels.com/2025/rlc-firebird-redline-wheels.jpg', 'detail', FALSE, 9, '2025-01-18 10:03:00');

-- ============================================
-- 12. СЕССИИ (для демонстрации)
-- ============================================

INSERT INTO user_sessions (user_id, token_hash, ip_address, user_agent, expires_at, created_at) VALUES
(1, 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6', '192.168.1.100', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)', '2025-12-09 02:18:00', '2025-12-08 02:18:00'),
(2, 'z9y8x7w6v5u4t3s2r1q0p9o8n7m6l5k4', '192.168.1.101', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)', '2025-12-09 02:18:00', '2025-12-08 02:18:00'),
(5, 'q1w2e3r4t5y6u7i8o9p0a1s2d3f4g5h6', '192.168.1.102', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)', '2025-12-09 02:18:00', '2025-12-08 02:18:00');

-- ============================================
-- ЗАВЕРШЕНИЕ СКРИПТА
-- ============================================

-- Обновление sequences
SELECT setval('manufacturers_manufacturer_id_seq', (SELECT MAX(manufacturer_id) FROM manufacturers));
SELECT setval('series_series_id_seq', (SELECT MAX(series_id) FROM series));
SELECT setval('castings_casting_id_seq', (SELECT MAX(casting_id) FROM castings));
SELECT setval('car_models_model_id_seq', (SELECT MAX(model_id) FROM car_models));
SELECT setval('users_user_id_seq', (SELECT MAX(user_id) FROM users));
SELECT setval('user_collections_collection_id_seq', (SELECT MAX(collection_id) FROM user_collections));
SELECT setval('wishlists_wishlist_id_seq', (SELECT MAX(wishlist_id) FROM wishlists));
SELECT setval('listings_listing_id_seq', (SELECT MAX(listing_id) FROM listings));
SELECT setval('transactions_transaction_id_seq', (SELECT MAX(transaction_id) FROM transactions));
SELECT setval('reviews_review_id_seq', (SELECT MAX(review_id) FROM reviews));
SELECT setval('model_images_image_id_seq', (SELECT MAX(image_id) FROM model_images));

-- Вывод статистики
SELECT 'Database populated successfully!' AS status;
SELECT 
    'Manufacturers: ' || COUNT(*) AS count FROM manufacturers
UNION ALL
SELECT 'Series: ' || COUNT(*) FROM series
UNION ALL
SELECT 'Castings: ' || COUNT(*) FROM castings
UNION ALL
SELECT 'Car Models: ' || COUNT(*) FROM car_models
UNION ALL
SELECT 'Users: ' || COUNT(*) FROM users
UNION ALL
SELECT 'Collections: ' || COUNT(*) FROM user_collections
UNION ALL
SELECT 'Wishlists: ' || COUNT(*) FROM wishlists
UNION ALL
SELECT 'Listings: ' || COUNT(*) FROM listings
UNION ALL
SELECT 'Transactions: ' || COUNT(*) FROM transactions
UNION ALL
SELECT 'Reviews: ' || COUNT(*) FROM reviews
UNION ALL
SELECT 'Images: ' || COUNT(*) FROM model_images;


\echo '✅ V005: Test data inserted successfully!'
