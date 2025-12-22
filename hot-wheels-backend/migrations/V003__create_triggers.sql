-- ============================================
-- V003: Create Triggers and Functions
-- Business logic at database level
-- ============================================

\echo '⚡ V003: Creating triggers and functions...'

-- Function: Update timestamp
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

\echo '  ✓ update_timestamp function created'

-- Triggers for updated_at
CREATE TRIGGER trg_car_models_update
BEFORE UPDATE ON car_models
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER trg_collections_update
BEFORE UPDATE ON user_collections
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

\echo '  ✓ updated_at triggers created'

-- Function: Auto-update listing status on transaction completion
CREATE OR REPLACE FUNCTION update_listing_status()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.payment_status = 'completed' AND (TG_OP = 'INSERT' OR OLD.payment_status != 'completed') THEN
        UPDATE listings 
        SET status = 'sold', sold_at = CURRENT_TIMESTAMP
        WHERE listing_id = NEW.listing_id AND status = 'active';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_transaction_complete
AFTER INSERT OR UPDATE ON transactions
FOR EACH ROW EXECUTE FUNCTION update_listing_status();

\echo '  ✓ listing status triggers created'

-- Function: Increment listing views
CREATE OR REPLACE FUNCTION increment_listing_views()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE listings 
    SET views_count = views_count + 1
    WHERE listing_id = NEW.listing_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

\echo '  ✓ increment_listing_views function created'

-- Function: Validate collection item for listing
CREATE OR REPLACE FUNCTION validate_listing_collection_item()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.collection_item_id IS NOT NULL THEN
        IF NOT EXISTS (
            SELECT 1 FROM user_collections 
            WHERE collection_id = NEW.collection_item_id 
            AND user_id = NEW.seller_id
            AND model_id = NEW.model_id
        ) THEN
            RAISE EXCEPTION 'Collection item does not belong to seller or model mismatch';
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validate_listing
BEFORE INSERT OR UPDATE ON listings
FOR EACH ROW EXECUTE FUNCTION validate_listing_collection_item();

\echo '  ✓ listing validation triggers created'

-- Function: Clean expired sessions
CREATE OR REPLACE FUNCTION clean_expired_sessions()
RETURNS void AS $$
BEGIN
    DELETE FROM user_sessions WHERE expires_at < CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;

\echo '  ✓ clean_expired_sessions function created'

-- Stored Procedure: Add to collection with validation
CREATE OR REPLACE FUNCTION add_to_collection(
    p_user_id INT,
    p_model_id INT,
    p_condition VARCHAR,
    p_price NUMERIC DEFAULT NULL,
    p_quantity INT DEFAULT 1
) RETURNS INT AS $$
DECLARE
    v_collection_id INT;
BEGIN
    -- Validate user
    IF NOT EXISTS (SELECT 1 FROM users WHERE user_id = p_user_id AND is_active = TRUE) THEN
        RAISE EXCEPTION 'User not found or inactive';
    END IF;
    
    -- Validate model
    IF NOT EXISTS (SELECT 1 FROM car_models WHERE model_id = p_model_id) THEN
        RAISE EXCEPTION 'Model not found';
    END IF;
    
    -- Insert collection item
    INSERT INTO user_collections (user_id, model_id, condition, acquisition_price, quantity)
    VALUES (p_user_id, p_model_id, p_condition, p_price, p_quantity)
    RETURNING collection_id INTO v_collection_id;
    
    RETURN v_collection_id;
END;
$$ LANGUAGE plpgsql;

\echo '  ✓ add_to_collection procedure created'

-- Function: Get user collection statistics
CREATE OR REPLACE FUNCTION get_user_collection_stats(p_user_id INT)
RETURNS TABLE(
    total_items BIGINT,
    total_value NUMERIC,
    common_count BIGINT,
    rare_count BIGINT,
    chase_count BIGINT,
    sth_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*)::BIGINT as total_items,
        COALESCE(SUM(uc.acquisition_price), 0) as total_value,
        COUNT(*) FILTER (WHERE cm.rarity_level = 'Common')::BIGINT as common_count,
        COUNT(*) FILTER (WHERE cm.rarity_level = 'Rare')::BIGINT as rare_count,
        COUNT(*) FILTER (WHERE cm.rarity_level = 'Chase')::BIGINT as chase_count,
        COUNT(*) FILTER (WHERE cm.rarity_level = 'Super Treasure Hunt')::BIGINT as sth_count
    FROM user_collections uc
    JOIN car_models cm ON uc.model_id = cm.model_id
    WHERE uc.user_id = p_user_id;
END;
$$ LANGUAGE plpgsql;

\echo '  ✓ get_user_collection_stats function created'

-- Function: Search models by text
CREATE OR REPLACE FUNCTION search_models(search_term TEXT)
RETURNS TABLE(
    model_id INT,
    casting_name VARCHAR,
    series_name VARCHAR,
    color VARCHAR,
    release_year INT,
    rarity_level VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        cm.model_id,
        c.casting_name,
        s.series_name,
        cm.color,
        cm.release_year,
        cm.rarity_level
    FROM car_models cm
    JOIN castings c ON cm.casting_id = c.casting_id
    LEFT JOIN series s ON cm.series_id = s.series_id
    WHERE 
        to_tsvector('english', c.casting_name) @@ plainto_tsquery('english', search_term)
        OR to_tsvector('english', COALESCE(s.series_name, '')) @@ plainto_tsquery('english', search_term)
        OR cm.color ILIKE '%' || search_term || '%'
    ORDER BY cm.release_year DESC, c.casting_name
    LIMIT 100;
END;
$$ LANGUAGE plpgsql;

\echo '  ✓ search_models function created'

\echo '✅ V003: All triggers and functions created successfully!'
