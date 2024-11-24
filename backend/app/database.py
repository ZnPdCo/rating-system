"""
Filename: database.py
Author: ZnPdCo
"""

import pymysql
from app.config import config


def connect_db():
    """
    Connect to the database and create tables if they don't exist.

    Returns:
        conn: Connection object to the database.
    """
    conn = pymysql.connect(
        host=config["db_host"],
        port=config["db_port"],
        user=config["db_user"],
        password=config["db_password"],
        db=config["db_name"],
        charset="utf8mb4",
    )
    cursor = conn.cursor()
    cursor.execute(
        """ 
CREATE TABLE IF NOT EXISTS problems (
pid INTEGER PRIMARY KEY AUTO_INCREMENT, 
contest VARCHAR(255), 
name VARCHAR(255), 
difficulty DOUBLE DEFAULT null,
quality DOUBLE DEFAULT null,
difficulty2 DOUBLE DEFAULT null,
quality2 DOUBLE DEFAULT null,
cnt1 INTEGER DEFAULT 0,
cnt2 INTEGER DEFAULT 0,
info VARCHAR(255),
OJpid VARCHAR(255) DEFAULT ""
); 
                """
    )
    cursor.execute(
        """ 
CREATE TABLE IF NOT EXISTS users (
id VARCHAR(255) PRIMARY KEY,
username VARCHAR(255),
password VARCHAR(255),
permission INTEGER DEFAULT 0,
status MEDIUMTEXT
); 
                """
    )
    cursor.execute(
        """ 
CREATE TABLE IF NOT EXISTS difficulty (
id VARCHAR(255) PRIMARY KEY,
username VARCHAR(255), 
pid INTEGER, 
val DOUBLE
); 
                """
    )
    cursor.execute(
        """ 
CREATE TABLE IF NOT EXISTS quality (
id VARCHAR(255) PRIMARY KEY,
username VARCHAR(255), 
pid INTEGER, 
val DOUBLE
); 
                """
    )
    cursor.execute(
        """ 
CREATE TABLE IF NOT EXISTS comment (
id VARCHAR(255) PRIMARY KEY,
username VARCHAR(255), 
pid INTEGER, 
val VARCHAR(255)
); 
                """
    )
    cursor.execute(
        """ 
CREATE TABLE IF NOT EXISTS report (
id VARCHAR(255),
pid INTEGER, 
difficulty DOUBLE,
quality DOUBLE,
comment VARCHAR(255),
username VARCHAR(255)
); 
                """
    )
    cursor.execute(
        """ 
CREATE TABLE IF NOT EXISTS verify (
id VARCHAR(255),
username VARCHAR(255),
password VARCHAR(255),
code VARCHAR(255),
created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 
                """
    )
    cursor.execute(
        """ 
CREATE TABLE IF NOT EXISTS announcement (
announcement TEXT
); 
                """
    )
    conn.commit()
    return conn
