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
	api_key varchar(20) NOT NULL,
	user_name varchar(100) NOT NULL,
	user_pwd varchar(100) NOT NULL,
	token text NULL,
    url text null,
    expiration integer null,
    other_urls text null,
	CONSTRAINT config_pkey PRIMARY KEY (api_key)
);

-- Permissions

ALTER TABLE elogapi.config
    OWNER TO iofmtadm;
GRANT ALL ON TABLE elogapi.config TO iofmtadm;

ALTER TABLE elogapi.config
    DROP COLUMN IF EXISTS user_pwd,
    ALTER COLUMN api_key TYPE TEXT,
    ADD COLUMN account_number    INTEGER NOT NULL,
    ADD COLUMN created_date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ADD COLUMN created_by        VARCHAR(255),
    ADD CONSTRAINT config_url_username_unique UNIQUE (url, user_name);
