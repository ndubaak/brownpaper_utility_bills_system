CREATE DATABASE IF NOT EXISTS test3db;

CREATE USER IF NOT EXISTS 'test2_user'@'localhost' IDENTIFIED BY 'name';
GRANT ALL PRIVILEGES ON test2db.* TO 'test2_user'@'localhost';
GRANT SELECT ON performance_schema.* TO 'test2_user'@'locahost';
FLUSH PRIVILEGES;