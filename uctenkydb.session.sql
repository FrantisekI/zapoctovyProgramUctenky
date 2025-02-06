-- DROP TABLE IF EXISTS ReceiptItems, Receipts, Users;
-- SHOW TABLES;


-- SELECT * FROM receiptitems;

-- DROP DATABASE uctenkydb;
-- CREATE DATABASE uctenkydb;

-- C:/Users/zapot/Documents/VŠ/programovani/programovaniCV/dbBackup

SELECT *
INTO OUTFILE 'C:/Users/zapot/Documents/VŠ/programovani/programovaniCV/dbBackup/backup.sql'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
FROM uctenkydb.receiptitems;