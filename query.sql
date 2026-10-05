ATTACH 'company_data.duckdb' AS my_database (READ_ONLY);
USE my_db;
SHOW TABLES;
SELECT * FROM employees LIMIT 100;