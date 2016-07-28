# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 15:29:52 2016

@author: nhuynh
"""

import sqlite3;
import pandas as pd;

#conn = sqlite3.connect('../newStation4/DefaultRun/results.mmdb');
#cur = conn.cursor();
#cur.execute("SELECT name FROM sqlite_master WHERE type='table';");
#conn.close();

def to_csv_all():
    db = sqlite3.connect('../newStation4/DefaultRun/results.mmdb')
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table_name in tables:
        table_name = table_name[0]
        table = pd.read_sql_query("SELECT * from %s" % table_name, db)
        table.to_csv(table_name + '.csv', index_label='index')

def to_csv_single(tablename):
    db = sqlite3.connect('../newStation4/DefaultRun/results.mmdb')
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    
    table = pd.read_sql_query("SELECT * from %s" %tablename, db)
    table.to_csv(tablename + '.csv', index_label='index')
    
    db.close();
    
to_csv_single('AgentInfo');

