-- ============================================
-- V002: Create Indexes
-- Performance optimization for frequent queries
-- ============================================

\echo '🔍 V002: Creating indexes...'

-- Indexes for car_models (most queried table)
CREATE INDEX IF NOT EXISTS idx_car_models_year ON car_models(release_year);
CREATE INDEX IF NOT EXISTS idx_car_models_series ON car_models(series_id);
CREATE INDEX IF NOT EXISTS idx_car_models_rarity ON car_models(rarity_level);
CREATE INDEX IF NOT EXISTS idx_car_models_casting ON car_models(casting_id);
CREATE INDEX IF NOT EXISTS idx_car_models_sku ON car_models(sku);

\echo '  ✓ car_models indexes created'

-- Composite index for common query patterns
CREATE INDEX IF NOT EXISTS idx_car_models_series_year ON car_models(series_id, release_year);
CREATE INDEX IF NOT EXISTS idx_car_models_rarity_year ON car_models(rarity_level, release_year);

\echo '  ✓ car_models composite indexes created'

-- Indexes for user_collections
CREATE INDEX IF NOT EXISTS idx_collections_user ON user_collections(user_id);
CREATE INDEX IF NOT EXISTS idx_collections_model ON user_collections(model_id);
CREATE INDEX IF NOT EXISTS idx_collections_for_sale ON user_collections(is_for_sale) WHERE is_for_sale = TRUE;
CREATE INDEX IF NOT EXISTS idx_collections_for_trade ON user_collections(is_for_trade) WHERE is_for_trade = TRUE;
CREATE INDEX IF NOT EXISTS idx_collections_user_model ON user_collections(user_id, model_id);

\echo '  ✓ user_collections indexes created'

-- Indexes for listings (marketplace queries)
CREATE INDEX IF NOT EXISTS idx_listings_active ON listings(status) WHERE status = 'active';
CREATE INDEX IF NOT EXISTS idx_listings_seller ON listings(seller_id);
CREATE INDEX IF NOT EXISTS idx_listings_model ON listings(model_id);
CREATE INDEX IF NOT EXISTS idx_listings_type ON listings(listing_type);
CREATE INDEX IF NOT EXISTS idx_listings_created ON listings(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_listings_expires ON listings(expires_at) WHERE expires_at IS NOT NULL;

\echo '  ✓ listings indexes created'

-- Composite indexes for listings
CREATE INDEX IF NOT EXISTS idx_listings_model_status ON listings(model_id, status);
CREATE INDEX IF NOT EXISTS idx_listings_seller_status ON listings(seller_id, status);

\echo '  ✓ listings composite indexes created'

-- Indexes for transactions
CREATE INDEX IF NOT EXISTS idx_transactions_buyer ON transactions(buyer_id);
CREATE INDEX IF NOT EXISTS idx_transactions_seller ON transactions(seller_id);
CREATE INDEX IF NOT EXISTS idx_transactions_listing ON transactions(listing_id);
CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_transactions_status ON transactions(payment_status);

\echo '  ✓ transactions indexes created'

-- Indexes for wishlists
CREATE INDEX IF NOT EXISTS idx_wishlists_user ON wishlists(user_id);
CREATE INDEX IF NOT EXISTS idx_wishlists_model ON wishlists(model_id);
CREATE INDEX IF NOT EXISTS idx_wishlists_priority ON wishlists(priority DESC);

\echo '  ✓ wishlists indexes created'

-- Indexes for reviews
CREATE INDEX IF NOT EXISTS idx_reviews_transaction ON reviews(transaction_id);
CREATE INDEX IF NOT EXISTS idx_reviews_reviewer ON reviews(reviewer_id);
CREATE INDEX IF NOT EXISTS idx_reviews_reviewee ON reviews(reviewee_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);

\echo '  ✓ reviews indexes created'

-- Indexes for model_images
CREATE INDEX IF NOT EXISTS idx_model_images_model ON model_images(model_id);
CREATE INDEX IF NOT EXISTS idx_model_images_type ON model_images(image_type);
CREATE INDEX IF NOT EXISTS idx_model_images_primary ON model_images(is_primary) WHERE is_primary = TRUE;
CREATE INDEX IF NOT EXISTS idx_model_images_uploader ON model_images(uploaded_by);

\echo '  ✓ model_images indexes created'

-- Indexes for sessions
CREATE INDEX IF NOT EXISTS idx_sessions_user ON user_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_expires ON user_sessions(expires_at);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON user_sessions(token_hash);

\echo '  ✓ user_sessions indexes created'

-- Indexes for series and castings
CREATE INDEX IF NOT EXISTS idx_series_manufacturer ON series(manufacturer_id);
CREATE INDEX IF NOT EXISTS idx_series_year ON series(release_year);
CREATE INDEX IF NOT EXISTS idx_castings_manufacturer ON castings(manufacturer_id);
CREATE INDEX IF NOT EXISTS idx_castings_year ON castings(first_release_year);

\echo '  ✓ series and castings indexes created'

-- Full-text search indexes (GIN)
CREATE INDEX IF NOT EXISTS idx_casting_name_gin ON castings USING gin(to_tsvector('english', casting_name));
CREATE INDEX IF NOT EXISTS idx_series_name_gin ON series USING gin(to_tsvector('english', series_name));
CREATE INDEX IF NOT EXISTS idx_listings_description_gin ON listings USING gin(to_tsvector('english', description));

\echo '  ✓ Full-text search indexes created'

-- Users indexes
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
CREATE INDEX IF NOT EXISTS idx_users_verified ON users(is_verified);
CREATE INDEX IF NOT EXISTS idx_users_country ON users(country);

\echo '  ✓ users indexes created'

\echo '✅ V002: All indexes created successfully!'
