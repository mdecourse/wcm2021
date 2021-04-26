
# 使用 peewee ORM
from peewee import SqliteDatabase, Model, CharField, TextField, IntegerField, MySQLDatabase
# for os.environ and os.system
import os

# 為了讓程式能夠同時在 Leo Editor 與 SciTE 中執行列印
# 特別建立 leoprint 函式
# *args 表示 leoprint 可以接受任意數量的輸入變數
def leoprint(*args):
    try:
        g.es(*args)
    except:
        print(*args)
        
ormdb = "sqlite"

if ormdb == "sqlite":
    # 針對 sqlite3 指定資料庫檔案
    db = SqliteDatabase("./course.db", check_same_thread=False)
    db.connection()

# 在此建立資料表欄位
class Course(Model):
    # peewee 內定 id 為 PrimaryKey
    #id = PrimaryKey()
    semester = CharField()
    classroomno = CharField()
    week = CharField()
    session = CharField()
    content = CharField()
    memo = TextField()

    class Meta:
        database = db # This model uses the ./+"course.db" database.   

# 對資料庫進行 select 查詢, 星期四電腦輔助設計室的排課內容, 依照排課節次由小到大排序
data = Course.select().where(Course.week=="4").order_by(Course.session)
# 關閉資料庫連線
db.close()
# 計算查詢結果總數
total_rows = data.count()
# 逐一列出各筆資料的排課內容
for i in range(total_rows):
    c = data[i]
    leoprint("第"+str(c.session)+"節:", c.content)