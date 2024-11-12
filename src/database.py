"""
Filename: database.py
Author: ZnPdCo
"""

import sqlite3 as sl


def connect_db():
    """
    Connect to the database and create tables if they don't exist.

    Returns:
        conn: Connection object to the database.
    """
    try:
        conn = sl.connect("rating.db", check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute(
            """ 
CREATE TABLE IF NOT EXISTS problems (
	pid INTEGER PRIMARY KEY AUTOINCREMENT, 
    contest VARCHAR(2048), 
    name VARCHAR(2048), 
    difficulty DOUBLE DEFAULT null,
    quality DOUBLE DEFAULT null,
    difficulty2 DOUBLE DEFAULT null,
    quality2 DOUBLE DEFAULT null,
    cnt1 INTEGER DEFAULT 0,
    cnt2 INTEGER DEFAULT 0,
    info json
); 
                    """
        )
        cursor.execute(
            """ 
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(2048) PRIMARY KEY,
    username VARCHAR(2048),
    password VARCHAR(2048),
    admin INTEGER DEFAULT 0
); 
                    """
        )
        cursor.execute(
            """ 
CREATE TABLE IF NOT EXISTS difficulty (
    id VARCHAR(2048) PRIMARY KEY,
	username VARCHAR(2048), 
    pid INTEGER, 
    val DOUBLE
    ); 
                    """
        )
        cursor.execute(
            """ 
CREATE TABLE IF NOT EXISTS quality (
    id VARCHAR(2048) PRIMARY KEY,
	username VARCHAR(2048), 
    pid INTEGER, 
    val DOUBLE
    ); 
                    """
        )
        cursor.execute(
            """ 
CREATE TABLE IF NOT EXISTS comment (
    id VARCHAR(2048) PRIMARY KEY,
	username VARCHAR(2048), 
    pid INTEGER, 
    val VARCHAR(2048)
    ); 
                    """
        )
        cursor.execute(
            """ 
CREATE TABLE IF NOT EXISTS report (
    id VARCHAR(2048),
    pid INTEGER, 
    difficulty DOUBLE,
    quality DOUBLE,
    comment VARCHAR(2048),
    username VARCHAR(2048)
    ); 
                    """
        )
        conn.commit()
    except sl.Error:
        conn = None
    return conn
