CREATE DATABASE SCHOOL;


-- @block
USE SCHOOL;

-- @block
CREATE TABLE time_table(
    name VARCHAR(255) NOT NULL,
    day INT NOT NULL CHECK (day >= 0 AND day <= 4),
    prd1 VARCHAR(255) ,
    prd2 VARCHAR(255) ,
    prd3 VARCHAR(255) ,
    prd4 VARCHAR(255) ,
    prd5 VARCHAR(255) ,
    prd6 VARCHAR(255) ,
    prd7 VARCHAR(255) ,
    prd8 VARCHAR(255) ,
    PRIMARY KEY (name, day));


--@block
INSERT INTO time_table 
VALUES (
'PARTH',
2,
'9A',
'12B',
'8D',
'9A',
'12B',
'8D',
'9A',
'12B'
) ;


--@block
INSERT INTO teacher_data
VALUES (
'PARH',
'abc'
) ;

--@block
CREATE TABLE teacher_data(
    name VARCHAR(255) NOT NULL UNIQUE PRIMARY KEY,
    departmet VARCHAR(255) NOT NULL
);


--@block
SELECT * FROM time_table;


--@block
SELECT * FROM teacher_data;

--@block
DROP TABLE time_table;

--@block
ALTER TABLE time_table name VARCHAR(255) NOT NULL PRIMARY KEY;

--@block
DROP DATABASE IF EXISTS ssa_db 
;

--@block
USE ssa_db
;

--@block
SELECT * FROM time_table;

--@block
SELECT * FROM time_table WHERE name = "Arushi Rege";