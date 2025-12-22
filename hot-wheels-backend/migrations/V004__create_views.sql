-- ============================================
-- V004: Create Views
-- Simplified queries and data access
-- ============================================

\echo '👁️  V004: Creating views...'

-- View: Masked user data (PII protection)
CREATE OR REPLACE VIEW users_masked AS
SELECT 
    user_id,
    username,
    CONCAT(LEFT(email, 3), '***@', SPLIT_PART(email, '@', 2)) AS email_masked,
    full_name,
    country,
    city,
    profile_image_url,
    bio,
    is_verified,
    role,
    created_at,
    last_login
FROM users
WHERE is_active = TRUE;

\echo '  ✓ users_masked view created'

-- View: Active marketplace listings with details
CREATE OR REPLACE VIEW active_listings_detail AS
SELECT 
    l.listing_id,
    l.seller_id,
    u.username as seller_username,
    u.country as seller_country,
    l.model_id,
    c.casting_name,
    s.series_name,
    cm.release_year,
    cm.color,
    cm.rarity_level,
    l.listing_type,
    l.price,
    l.condition,
    l.description,
    l.views_count,
    l.created_at,
    l.expires_at,
    CASE 
        WHEN l.expires_at < CURRENT_TIMESTAMP THEN TRUE
        ELSE FALSE
    END as is_expired
FROM listings l
JOIN users u ON l.seller_id = u.user_id
JOIN car_models cm ON l.model_id = cm.model_id
JOIN castings c ON cm.casting_id = c.casting_id
LEFT JOIN series s ON cm.series_id = s.series_id
WHERE l.status = 'active';

\echo '  ✓ active_listings_detail view created'

-- View: User collection with model details
CREATE OR REPLACE VIEW user_collection_detail AS
SELECT 
    uc.collection_id,
    uc.user_id,
    u.username,
    uc.model_id,
    c.casting_name,
    s.series_name,
    cm.release_year,
    cm.color,
    cm.rarity_level,
    cm.msrp,
    uc.acquisition_date,
    uc.acquisition_price,
    uc.condition,
    uc.is_in_package,
    uc.quantity,
    uc.is_for_trade,
    uc.is_for_sale,
    uc.storage_location,
    uc.notes
FROM user_collections uc
JOIN users u ON uc.user_id = u.user_id
JOIN car_models cm ON uc.model_id = cm.model_id
JOIN castings c ON cm.casting_id = c.casting_id
LEFT JOIN series s ON cm.series_id = s.series_id;

\echo '  ✓ user_collection_detail view created'

-- View: Transaction history with details
CREATE OR REPLACE VIEW transaction_history AS
SELECT 
    t.transaction_id,
    t.listing_id,
    t.buyer_id,
    buyer.username as buyer_username,
    t.seller_id,
    seller.username as seller_username,
    cm.model_id,
    c.casting_name,
    cm.color,
    cm.rarity_level,
    t.transaction_type,
    t.amount,
    t.payment_status,
    t.shipping_status,
    t.tracking_number,
    t.created_at,
    t.completed_at
FROM transactions t
JOIN users buyer ON t.buyer_id = buyer.user_id
JOIN users seller ON t.seller_id = seller.user_id
JOIN listings l ON t.listing_id = l.listing_id
JOIN car_models cm ON l.model_id = cm.model_id
JOIN castings c ON cm.casting_id = c.casting_id;

\echo '  ✓ transaction_history view created'

-- View: User ratings summary
CREATE OR REPLACE VIEW user_ratings_summary AS
SELECT 
    u.user_id,
    u.username,
    COUNT(r.review_id) as total_reviews,
    ROUND(AVG(r.rating)::numeric, 2) as average_rating,
    COUNT(*) FILTER (WHERE r.rating = 5) as five_star_count,
    COUNT(*) FILTER (WHERE r.rating = 4) as four_star_count,
    COUNT(*) FILTER (WHERE r.rating = 3) as three_star_count,
    COUNT(*) FILTER (WHERE r.rating <= 2) as low_rating_count
FROM users u
LEFT JOIN reviews r ON u.user_id = r.reviewee_id
GROUP BY u.user_id, u.username;

\echo '  ✓ user_ratings_summary view created'

-- View: Popular models (most collected)
CREATE OR REPLACE VIEW popular_models AS
SELECT 
    cm.model_id,
    c.casting_name,
    s.series_name,
    cm.release_year,
    cm.color,
    cm.rarity_level,
    COUNT(DISTINCT uc.user_id) as collectors_count,
    COUNT(uc.collection_id) as total_in_collections,
    COUNT(DISTINCT w.user_id) as wishlist_count,
    COUNT(DISTINCT l.listing_id) as active_listings_count
FROM car_models cm
JOIN castings c ON cm.casting_id = c.casting_id
LEFT JOIN series s ON cm.series_id = s.series_id
LEFT JOIN user_collections uc ON cm.model_id = uc.model_id
LEFT JOIN wishlists w ON cm.model_id = w.model_id
LEFT JOIN listings l ON cm.model_id = l.model_id AND l.status = 'active'
GROUP BY cm.model_id, c.casting_name, s.series_name, cm.release_year, cm.color, cm.rarity_level
ORDER BY collectors_count DESC, wishlist_count DESC;

\echo '  ✓ popular_models view created'

-- Materialized View: Market price statistics (refreshed periodically)
CREATE MATERIALIZED VIEW IF NOT EXISTS market_price_stats AS
SELECT 
    cm.model_id,
    c.casting_name,
    cm.release_year,
    cm.rarity_level,
    cm.msrp,
    COUNT(t.transaction_id) as total_sales,
    ROUND(AVG(t.amount)::numeric, 2) as avg_sale_price,
    ROUND(MIN(t.amount)::numeric, 2) as min_sale_price,
    ROUND(MAX(t.amount)::numeric, 2) as max_sale_price,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY t.amount)::numeric, 2) as median_sale_price,
    MAX(t.completed_at) as last_sale_date
FROM car_models cm
JOIN castings c ON cm.casting_id = c.casting_id
JOIN listings l ON cm.model_id = l.model_id
JOIN transactions t ON l.listing_id = t.listing_id
WHERE t.payment_status = 'completed'
GROUP BY cm.model_id, c.casting_name, cm.release_year, cm.rarity_level, cm.msrp
HAVING COUNT(t.transaction_id) >= 1;

-- Create index on materialized view
CREATE INDEX IF NOT EXISTS idx_market_stats_model ON market_price_stats(model_id);
CREATE INDEX IF NOT EXISTS idx_market_stats_rarity ON market_price_stats(rarity_level);

\echo '  ✓ market_price_stats materialized view created'

-- View: Seller performance metrics
CREATE OR REPLACE VIEW seller_performance AS
SELECT 
    u.user_id,
    u.username,
    COUNT(DISTINCT l.listing_id) as total_listings,
    COUNT(DISTINCT l.listing_id) FILTER (WHERE l.status = 'active') as active_listings,
    COUNT(DISTINCT l.listing_id) FILTER (WHERE l.status = 'sold') as sold_listings,
    COUNT(DISTINCT t.transaction_id) as total_transactions,
    COALESCE(SUM(t.amount) FILTER (WHERE t.payment_status = 'completed'), 0) as total_revenue,
    ROUND(AVG(r.rating)::numeric, 2) as seller_rating,
    COUNT(r.review_id) as review_count
FROM users u
LEFT JOIN listings l ON u.user_id = l.seller_id
LEFT JOIN transactions t ON l.listing_id = t.listing_id
LEFT JOIN reviews r ON u.user_id = r.reviewee_id
WHERE u.role IN ('trader', 'collector')
GROUP BY u.user_id, u.username;

\echo '  ✓ seller_performance view created'

\echo '✅ V004: All views created successfully!'
