/*
This script creates a table named 'config' in the 'public' schema if it does not already exist. 
The 'config' table is designed to store configuration details with the following columns:
- api_key: A varchar(20) that serves as the primary key.
- user_name: A varchar(255) to store the name of the api user.
- user_pwd: A varchar(255) to store the password of the api user.
- token: access token.
- url: utl to access elogs api.
- expiration: time to expire token.

Additionally, the script sets the owner of the 'config' table to 'iofmtadm' and grants all permissions on the table to 'iofmtadm'.
*/
CREATE TABLE IF NOT EXISTS elogapi.config (
    user_id SERIAL PRIMARY KEY,
    api_key TEXT UNIQUE NOT NULL,
    user_name VARCHAR(100) NOT NULL,
    token TEXT NULL,
    url TEXT NULL,
    expiration INTEGER NULL,
    other_urls TEXT NULL,
    account_number INTEGER NOT NULL,
    created_date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255),
    updated_date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_by VARCHAR(255),
    CONSTRAINT config_url_username_unique UNIQUE (url, user_name)
);

ALTER TABLE elogapi.config OWNER TO iofmtadm;
GRANT ALL ON TABLE elogapi.config TO iofmtadm;