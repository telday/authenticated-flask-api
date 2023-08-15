-- Create our base database/user and grant rights
CREATE DATABASE api;
CREATE USER flask SUPERUSER;
GRANT ALL PRIVILEGES ON DATABASE api TO flask;
