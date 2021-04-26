import os
# sqlite3 模組為 Python3 內建
import sqlite3
 

# 為了讓程式能夠同時在 Leo Editor 與 SciTE 中執行列印
# 特別建立 leoprint 函式
# *args 表示 leoprint 可以接受任意數量的輸入變數
def leoprint(*args):
    try:
        g.es(*args)
    except:
        print(*args)
 
# 資料庫檔案將與程式放在同一目錄
data_dir = "./"
 
class Init(object):
    def __init__(self):
        # 資料庫選用
        # 內建使用 sqlite3                
        ormdb = "sqlite"
        #ormdb = "mysql"
        #ormdb = "postgresql"
     
        if ormdb == "sqlite":
            # 資料庫使用 SQLite
            # ORM 只能建立資料表, 無法直接建立資料庫
            # 因此 MySQL 資料庫採 pymysql 建立
            # SQLite 資料庫採 sqlite3 建立
            # PostgreSQL 資料庫採 psycopg2 建立
            # 也可以使用 peewee 建立資料表格
            try:
                conn = sqlite3.connect(data_dir+"course.db")
                cur = conn.cursor()
                # 建立資料表
                cur.execute("CREATE TABLE IF NOT EXISTS course( \
                        id INTEGER PRIMARY KEY AUTOINCREMENT, \
                        semester TEXT, \
                        classroomno TEXT, \
                        week TEXT, \
                        session TEXT, \
                        content TEXT, \
                        memo TEXT);")
                cur.close()
                conn.close()
            except:
                leoprint("can not create db and table")
     
# 建立案例
init = Init()
leoprint("done")
