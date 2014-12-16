CREATE USER icinga WITH ENCRYPTED PASSWORD 'icinga' ;
CREATE DATABASE icinga WITH OWNER icinga ;
\c icinga;
SET ROLE icinga;

