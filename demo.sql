-- CREATE USER TABLE
CREATE TABLE IF NOT EXISTS beer_user (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    password TEXT,
    UNIQUE(name)
);

-- CREATE BEER SHOP TABLE
CREATE TABLE IF NOT EXISTS beer_shop (
    id INTEGER PRIMARY KEY,
    name TEXT
);


-- CREATE BEER TABLE
CREATE TABLE IF NOT EXISTS beer_review (
    id INTEGER PRIMARY KEY,
    user_id INT NOT NULL,
    shop_id INT NOT NULL,
    beer_name TEXT NOT NULL,
    review TEXT,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES beer_user(id),
    FOREIGN KEY(shop_id) REFERENCES beer_shop(id)
);


