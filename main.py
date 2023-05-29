#! /bin/python3

import requests
import time
import os
import datetime
from SQLite import SQLite
import argparse
import sys

sql = SQLite('database.sqlite')

def createTable(table):
    query = f"""CREATE TABLE `{table}` (
	`url` VARCHAR(255) NOT NULL,
	`status_code` INT(3) NOT NULL,
	`time_exec` TIME NOT NULL,
	`created_at` DATETIME NOT NULL DEFAULT(current_timestamp)
    );"""
    return sql.execute(query)

def getRequest(url:str):
    return requests.get(url)

def insert(url:str, status_code:int, time_exec:str):
    query = f"""INSERT INTO test (url, status_code, time_exec) VALUES
        ('{url}', {status_code}, '{time_exec}');
        """
    sql.execute(query)
    sql.commit()

if __name__ == "__main__":
    db_name = 'database.sqlite'
    url = 'https://sezoncentr.ru/'
    time_wait = 5
    parser = argparse.ArgumentParser(prog="SiteAvability", description="Description", epilog="text at the bottom of file")
    parser.add_argument('--url', help="URL", type=str)
    parser.add_argument('--sleep', help="Wait time between requests", type=int, default=60)
    parser.add_argument('--database', help="SQLite database file", type=str, default='database.sqlite')
    parser.add_argument('--table', help="Table name", type=str, default='test')
    parser.add_argument('--number', help="Number of requests", type=int, default=float('inf'))
    args = parser.parse_args()
    
    tries = 0;
    while(tries < args.number):
        start = datetime.datetime.now()
        response = getRequest(args.url)
        end = datetime.datetime.now()
        time_exec = end - start
        print(url, response.status_code, time_exec)
        insert(url, response.status_code, time_exec)
        tries = tries + 1 
        time.sleep(args.sleep)

    print('Progam successfuly terminated')
