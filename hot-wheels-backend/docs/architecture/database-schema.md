# Database Schema Documentation

This document describes the database schema for the Hot Wheels Collector API.

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                          ENTITY RELATIONSHIP DIAGRAM                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│    ┌──────────────┐                    ┌──────────────┐                         │
│    │ MANUFACTURER │                    │    SERIES    │                         │
│    ├──────────────┤                    ├──────────────┤                         │
│    │ manufacturerid│◄───┐        ┌────►│ seriesid     │                         │
│    │ name          │    │        │     │ seriesname   │                         │
│    │ country       │    │        │     │ releaseyear  │                         │
│    │ foundedyear   │    │        │     │ manufacturerid│───────┐                │
│    └──────────────┘    │        │     │ islimiteded. │       │                │
│                         │        │     └──────────────┘       │                │
│                         │        │            │               │                │
│    ┌──────────────┐    │        │            │               │                │
│    │   CASTING    │    │        │            │               │                │
│    ├──────────────┤    │        │            │               │                │
│    │ castingid    │◄───┼────────┼────────┐   │               │                │
│    │ castingname  │    │        │        │   │               │                │
│    │ firstrelease │    │        │        │   │               │                │
│    │ manufacturerid├───┘        │        │   │               │                │
│    │ scale        │             │        │   │               │                │
│    │ designer     │             │        │   │               │                │
│    │ basedonreal  │             │        │   │               │                │
│    └──────────────┘             │        │   │               │                │
│                                  │        │   │               │                │
│                                  │        │   ▼               │                │
│                          ┌───────┴────────┴─────────┐        │                │
│                          │        CARMODEL          │        │                │
│                          ├──────────────────────────┤        │                │
│                          │ modelid                  │        │                │
│                          │ castingid ───────────────┼────────┘                │
│                          │ seriesid ────────────────┤                         │
│                          │ releaseyear              │                         │
│                          │ color                    │                         │
│                          │ tampodesign              │                         │
│                          │ wheeltype                │                         │
│                          │ raritylevel              │                         │
│                          │ sku                      │                         │
│                          │ msrp                     │                         │
│                          └────────────┬─────────────┘                         │
│                                       │                                        │
│                    ┌──────────────────┼──────────────────┐                    │
│                    │                  │                  │                    │
│                    ▼                  ▼                  ▼                    │
│    ┌───────────────────┐  ┌───────────────────┐  ┌──────────────┐            │
│    │  USERCOLLECTION   │  │     WISHLIST      │  │   LISTING    │            │
│    ├───────────────────┤  ├───────────────────┤  ├──────────────┤            │
│    │ collectionid      │  │ wishlistid        │  │ listingid    │◄─────┐     │
│    │ userid ───────┐   │  │ userid ───────┐   │  │ sellerid ────┼──┐   │     │
│    │ modelid       │   │  │ modelid       │   │  │ modelid      │  │   │     │
│    │ acquisitiondt │   │  │ priority      │   │  │ collectionid │  │   │     │
│    │ condition     │   │  │ maxpricewill. │   │  │ listingtype  │  │   │     │
│    │ isinpackage   │   │  │ notes         │   │  │ price        │  │   │     │
│    │ isfortrade    │   │  └───────────────┼───┘  │ condition    │  │   │     │
│    │ isforsale     │   │                  │      │ status       │  │   │     │
│    └───────────────┼───┘                  │      └──────────────┘  │   │     │
│                    │                      │                        │   │     │
│                    │   ┌──────────────────┴────────────────┐       │   │     │
│                    │   │              USER                 │       │   │     │
│                    │   ├───────────────────────────────────┤       │   │     │
│                    └───┤ userid                            │◄──────┘   │     │
│                        │ username                          │           │     │
│                        │ email                             │           │     │
│                        │ passwordhash                      │           │     │
│                        │ fullname                          │           │     │
│                        │ role                              │           │     │
│                        │ isverified                        │           │     │
│                        └───────────────┬───────────────────┘           │     │
│                                        │                               │     │
│                    ┌───────────────────┴───────────────────┐           │     │
│                    │                                       │           │     │
│                    ▼                                       ▼           │     │
│    ┌───────────────────────┐              ┌───────────────────────┐   │     │
│    │      TRANSACTION      │              │        REVIEW         │   │     │
│    ├───────────────────────┤              ├───────────────────────┤   │     │
│    │ transactionid         │◄─────────────┤ reviewid              │   │     │
│    │ listingid ────────────┼──────────────┼───────────────────────┼───┘     │
│    │ buyerid               │              │ transactionid         │         │
│    │ sellerid              │              │ reviewerid            │         │
│    │ transactiontype       │              │ revieweeid            │         │
│    │ amount                │              │ rating                │         │
│    │ paymentstatus         │              │ comment               │         │
│    │ shippingstatus        │              └───────────────────────┘         │
│    └───────────────────────┘                                                 │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Tables

### users

Stores platform user information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `userid` | INTEGER | PK, AUTO_INCREMENT | Unique user identifier |
| `username` | VARCHAR(50) | UNIQUE, NOT NULL, INDEX | Display username |
| `email` | VARCHAR(150) | UNIQUE, NOT NULL, INDEX | Email address |
| `passwordhash` | VARCHAR(255) | NOT NULL | Bcrypt password hash |
| `fullname` | VARCHAR(150) | | Full name |
| `country` | VARCHAR(50) | | Country of residence |
| `city` | VARCHAR(100) | | City of residence |
| `profileimageurl` | TEXT | | Profile image URL |
| `bio` | TEXT | | User biography |
| `isverified` | BOOLEAN | DEFAULT FALSE | Email verification status |
| `isactive` | BOOLEAN | DEFAULT TRUE | Account active status |
| `role` | VARCHAR(20) | DEFAULT 'collector' | User role |
| `createdat` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |
| `lastlogin` | TIMESTAMP | | Last login timestamp |

**Constraints:**
- `CHECK (role IN ('collector', 'trader', 'admin', 'moderator'))`
- `CHECK (email ~ valid_email_pattern)`

**Indexes:**
- `idx_users_username` on `username`
- `idx_users_email` on `email`

### manufacturers

Stores toy car manufacturer information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `manufacturerid` | INTEGER | PK, AUTO_INCREMENT | Unique identifier |
| `name` | VARCHAR(100) | UNIQUE, NOT NULL | Manufacturer name |
| `country` | VARCHAR(50) | | Country of origin |
| `foundedyear` | INTEGER | | Year founded |
| `createdat` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |

### castings

Stores Hot Wheels casting (mold/tooling) information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `castingid` | INTEGER | PK, AUTO_INCREMENT | Unique identifier |
| `castingname` | VARCHAR(200) | NOT NULL | Casting name |
| `firstreleaseyear` | INTEGER | NOT NULL | Year first released |
| `manufacturerid` | INTEGER | FK → manufacturers | Manufacturer reference |
| `scale` | VARCHAR(10) | DEFAULT '1:64' | Scale ratio |
| `designer` | VARCHAR(100) | | Designer name |
| `basedonrealcar` | BOOLEAN | DEFAULT FALSE | Real car basis flag |
| `realcarmodel` | VARCHAR(200) | | Real car model name |
| `createdat` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |

**Constraints:**
- `CHECK (firstreleaseyear >= 1968)`

### series

Stores Hot Wheels series information.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `seriesid` | INTEGER | PK, AUTO_INCREMENT | Unique identifier |
| `seriesname` | VARCHAR(150) | NOT NULL | Series name |
| `releaseyear` | INTEGER | NOT NULL | Release year |
| `manufacturerid` | INTEGER | FK → manufacturers | Manufacturer reference |
| `description` | TEXT | | Series description |
| `islimitededition` | BOOLEAN | DEFAULT FALSE | Limited edition flag |
| `createdat` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |

**Constraints:**
- `CHECK (releaseyear >= 1968)`
- `UNIQUE (seriesname, releaseyear)`

### carmodels

Stores specific car model variants.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `modelid` | INTEGER | PK, AUTO_INCREMENT | Unique identifier |
| `castingid` | INTEGER | FK → castings, NOT NULL | Casting reference |
| `seriesid` | INTEGER | FK → series | Series reference |
| `releaseyear` | INTEGER | NOT NULL | Release year |
| `color` | VARCHAR(50) | NOT NULL | Primary color |
| `tampodesign` | VARCHAR(200) | | Tampo/decal design |
| `wheeltype` | VARCHAR(100) | | Wheel type |
| `basecolor` | VARCHAR(50) | | Base plate color |
| `windowcolor` | VARCHAR(50) | | Window color |
| `interiorcolor` | VARCHAR(50) | | Interior color |
| `productioncode` | VARCHAR(10) | | Production code |
| `sku` | VARCHAR(50) | UNIQUE | Stock keeping unit |
| `raritylevel` | VARCHAR(20) | | Rarity classification |
| `estimatedproductionquantity` | INTEGER | | Estimated quantity |
| `msrp` | DECIMAL(10,2) | | Suggested retail price |
| `createdat` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |
| `updatedat` | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

**Constraints:**
- `CHECK (raritylevel IN ('Common', 'Uncommon', 'Rare', 'Chase', 'Super Treasure Hunt'))`
- `UNIQUE (castingid, seriesid, releaseyear, color, tampodesign)`

**Indexes:**
- `idx_carmodels_casting` on `castingid`
- `idx_carmodels_series` on `seriesid`
- `idx_carmodels_year` on `releaseyear`
- `idx_carmodels_rarity` on `raritylevel`

### usercollections

Stores user's personal collection items.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `collectionid` | INTEGER | PK, AUTO_INCREMENT | Unique identifier |
| `userid` | INTEGER | FK → users, NOT NULL, INDEX | User reference |
| `modelid` | INTEGER | FK → carmodels, NOT NULL | Model reference |
| `acquisitiondate` | DATE | DEFAULT NOW() | Date acquired |
| `acquisitionprice` | DECIMAL(10,2) | | Purchase price |
| `condition` | VARCHAR(20) | | Item condition |
| `isinpackage` | BOOLEAN | DEFAULT TRUE | In original packaging |
| `packagecondition` | VARCHAR(20) | | Package condition |
| `quantity` | INTEGER | DEFAULT 1 | Number of items |
| `storagelocation` | VARCHAR(100) | | Storage location |
| `notes` | TEXT | | Additional notes |
| `isfortrade` | BOOLEAN | DEFAULT FALSE, INDEX | Available for trade |
| `isforsale` | BOOLEAN | DEFAULT FALSE, INDEX | Available for sale |
| `createdat` | TIMESTAMP | DEFAULT NOW() | Creation timestamp |
| `updatedat` | TIMESTAMP | DEFAULT NOW() | Last update timestamp |

**Constraints:**
- `CHECK (condition IN ('Mint', 'Near Mint', 'Excellent', 'Good', 'Fair', 'Poor'))`
- `CHECK (quantity > 0)`
- `UNIQUE (userid, modelid, acquisitiondate)`

### wishlists

Stores user's wishlist items.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `wishlistid` | INTEGER | PK, AUTO_INCREMENT | Unique identifier |
| `userid` | INTEGER | FK → users, NOT NULL, INDEX | User reference |
| `modelid` | INTEGER | FK → carmodels, NOT NULL | Model reference |
| `priority` | INTEGER | | Priority level (1-5) |
| `maxpricewilling` | DECIMAL(10,2) | | Maximum price willing |
| `notes` | TEXT | | Additional notes |
| `createdat` | TIMESTAMP | DEFAULT NOW() | Creation timestamp |

**Constraints:**
- `CHECK (priority BETWEEN 1 AND 5)`
- `CHECK (maxpricewilling >= 0)`
- `UNIQUE (userid, modelid)`

### listings

Stores marketplace listings.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `listingid` | INTEGER | PK, AUTO_INCREMENT | Unique identifier |
| `sellerid` | INTEGER | FK → users, NOT NULL, INDEX | Seller reference |
| `collectionitemid` | INTEGER | FK → usercollections | Collection item reference |
| `modelid` | INTEGER | FK → carmodels, NOT NULL, INDEX | Model reference |
| `listingtype` | VARCHAR(20) | NOT NULL | Listing type |
| `price` | DECIMAL(10,2) | | Sale price |
| `condition` | VARCHAR(20) | NOT NULL | Item condition |
| `description` | TEXT | | Listing description |
| `status` | VARCHAR(20) | DEFAULT 'active', INDEX | Listing status |
| `viewscount` | INTEGER | DEFAULT 0 | View counter |
| `createdat` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |
| `expiresat` | TIMESTAMP | | Expiration timestamp |
| `soldat` | TIMESTAMP | | Sale timestamp |

**Constraints:**
- `CHECK (listingtype IN ('sale', 'trade', 'auction'))`
- `CHECK (price IS NULL OR price > 0)`
- `CHECK (status IN ('active', 'sold', 'cancelled', 'expired'))`
- `CHECK (condition IN ('Mint', 'Near Mint', 'Excellent', 'Good', 'Fair', 'Poor'))`

### transactions

Stores completed marketplace transactions.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `transactionid` | INTEGER | PK, AUTO_INCREMENT | Unique identifier |
| `listingid` | INTEGER | FK → listings, NOT NULL | Listing reference |
| `buyerid` | INTEGER | FK → users, NOT NULL, INDEX | Buyer reference |
| `sellerid` | INTEGER | FK → users, NOT NULL, INDEX | Seller reference |
| `transactiontype` | VARCHAR(20) | NOT NULL | Transaction type |
| `amount` | DECIMAL(10,2) | NOT NULL | Transaction amount |
| `paymentmethod` | VARCHAR(50) | | Payment method |
| `paymentstatus` | VARCHAR(20) | DEFAULT 'pending' | Payment status |
| `shippingstatus` | VARCHAR(20) | DEFAULT 'not_shipped' | Shipping status |
| `trackingnumber` | VARCHAR(100) | | Tracking number |
| `createdat` | TIMESTAMP | NOT NULL, DEFAULT NOW(), INDEX | Creation timestamp |
| `completedat` | TIMESTAMP | | Completion timestamp |

**Constraints:**
- `CHECK (transactiontype IN ('purchase', 'trade'))`
- `CHECK (amount >= 0)`
- `CHECK (paymentstatus IN ('pending', 'completed', 'failed', 'refunded'))`
- `CHECK (shippingstatus IN ('not_shipped', 'shipped', 'in_transit', 'delivered'))`
- `CHECK (buyerid != sellerid)`

### reviews

Stores transaction reviews.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `reviewid` | INTEGER | PK, AUTO_INCREMENT | Unique identifier |
| `transactionid` | INTEGER | FK → transactions, NOT NULL | Transaction reference |
| `reviewerid` | INTEGER | FK → users, NOT NULL | Reviewer reference |
| `revieweeid` | INTEGER | FK → users, NOT NULL | Reviewee reference |
| `rating` | INTEGER | NOT NULL | Rating (1-5) |
| `comment` | TEXT | | Review comment |
| `createdat` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Creation timestamp |

**Constraints:**
- `CHECK (rating BETWEEN 1 AND 5)`
- `UNIQUE (transactionid, reviewerid)`

## Database Views

### v_active_listings

Active marketplace listings with seller and model details.

```sql
CREATE VIEW v_active_listings AS
SELECT 
    l.listingid,
    l.listingtype,
    l.price,
    l.condition,
    l.status,
    l.viewscount,
    l.createdat,
    u.username AS seller_username,
    u.isverified AS seller_verified,
    cm.color,
    cm.raritylevel,
    c.castingname
FROM listings l
JOIN users u ON l.sellerid = u.userid
JOIN carmodels cm ON l.modelid = cm.modelid
JOIN castings c ON cm.castingid = c.castingid
WHERE l.status = 'active';
```

### v_user_collection_summary

User collection summary with statistics.

```sql
CREATE VIEW v_user_collection_summary AS
SELECT 
    u.userid,
    u.username,
    COUNT(uc.collectionid) AS total_items,
    SUM(uc.quantity) AS total_quantity,
    SUM(uc.acquisitionprice * uc.quantity) AS total_value,
    COUNT(CASE WHEN uc.isfortrade THEN 1 END) AS items_for_trade,
    COUNT(CASE WHEN uc.isforsale THEN 1 END) AS items_for_sale
FROM users u
LEFT JOIN usercollections uc ON u.userid = uc.userid
GROUP BY u.userid, u.username;
```

## Triggers

### update_listing_sold

Updates listing status when transaction is created.

```sql
CREATE FUNCTION update_listing_sold() RETURNS TRIGGER AS $$
BEGIN
    UPDATE listings 
    SET status = 'sold', soldat = NOW()
    WHERE listingid = NEW.listingid;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_transaction_created
AFTER INSERT ON transactions
FOR EACH ROW EXECUTE FUNCTION update_listing_sold();
```

### update_timestamps

Automatically updates `updatedat` column.

```sql
CREATE FUNCTION update_timestamp() RETURNS TRIGGER AS $$
BEGIN
    NEW.updatedat = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_carmodels_updated
BEFORE UPDATE ON carmodels
FOR EACH ROW EXECUTE FUNCTION update_timestamp();
```

## Indexes Summary

| Table | Index Name | Columns | Type |
|-------|------------|---------|------|
| users | idx_users_username | username | UNIQUE |
| users | idx_users_email | email | UNIQUE |
| carmodels | idx_carmodels_casting | castingid | B-TREE |
| carmodels | idx_carmodels_series | seriesid | B-TREE |
| carmodels | idx_carmodels_year | releaseyear | B-TREE |
| carmodels | idx_carmodels_rarity | raritylevel | B-TREE |
| usercollections | idx_collection_user | userid | B-TREE |
| usercollections | idx_collection_trade | isfortrade | B-TREE |
| usercollections | idx_collection_sale | isforsale | B-TREE |
| listings | idx_listings_seller | sellerid | B-TREE |
| listings | idx_listings_model | modelid | B-TREE |
| listings | idx_listings_status | status | B-TREE |
| transactions | idx_transactions_buyer | buyerid | B-TREE |
| transactions | idx_transactions_seller | sellerid | B-TREE |
| transactions | idx_transactions_created | createdat | B-TREE |

---

**Next:** [API Reference](../reference/api-overview.md) | [Request Flow](request-flow.md)

