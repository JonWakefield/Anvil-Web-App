-- create database if not exists
CREATE DATABASE IF NOT EXISTS camera_nodes;
USE camera_nodes;
-- ADD OTHER sql COMMANDS to initialize if needed

-- create user `ginuser`
CREATE USER 'ginuser'@'maria-db' IDENTIFIED BY 'Hello2018';
GRANT ALL PRIVILEGES ON camera_nodes.* TO 'ginuser'@'maria-db';
FLUSH PRIVILEGES;
