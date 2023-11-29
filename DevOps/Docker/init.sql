-- create database if not exists
CREATE DATABASE IF NOT EXISTS camera_nodes;
USE camera_nodes;
-- ADD OTHER sql COMMANDS to initialize if needed

-- create user `'cotton_user'`
CREATE USER 'cotton_user'@'maria-db' IDENTIFIED BY 'db1234';
GRANT ALL PRIVILEGES ON camera_nodes.* TO 'cotton_user'@'maria-db';
FLUSH PRIVILEGES;
