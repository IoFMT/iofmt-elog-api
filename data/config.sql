/*
This script creates a table named 'config' in the 'public' schema if it does not already exist. 
The 'config' table is designed to store configuration details with the following columns:
- api_key: A varchar(20) that serves as the primary key.
- customer_name: A varchar(255) to store the name of the customer.
- access_token: A varchar(255) to store the access token.
- shared_links: A text field that can be null, used to store shared links.
- sfg_environment: A varchar(20) that can be null, used to store the environment information.

Additionally, the script sets the owner of the 'config' table to 'iofmtadm' and grants all permissions on the table to 'iofmtadm'.
*/
CREATE TABLE IF NOT EXISTS elogapi.config (
	api_key varchar(20) NOT NULL,
	user_name varchar(100) NOT NULL,
	user_pwd varchar(100) NOT NULL,
	token text NULL,
	CONSTRAINT config_pkey PRIMARY KEY (api_key)
);

-- Permissions

ALTER TABLE elogapi.config OWNER TO iofmtadm;
GRANT ALL ON TABLE elogapi.config TO iofmtadm;