DROP TABLE IF EXISTS item
DROP TABLE IF EXISTS cart 

CREATE TABLE item(
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price INTEGER NOT NULL,
    inventory_count INTEGER NOT NULL,
    
);

-- CREATE TABLE cart( 
--     cart_id INTEGER PRIMARY KEY AUTOINCREMENT,

-- );

