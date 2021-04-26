<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2"/>
<globals/>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="yen.20210426151453.1"><vh>@settings</vh>
<v t="yen.20210426151453.2"><vh>@data qt-gui-plugin-style-sheet</vh></v>
<v t="yen.20210426151453.3"><vh>@string initial_split_orientation = horizontal</vh></v>
</v>
<v t="yen.20210426151436.1"><vh>About</vh>
<v t="yen.20210426152501.1"><vh>以 clean 進行編輯</vh></v>
<v t="yen.20210426152321.1"><vh>@clean w1_create_db.py</vh>
<v t="yen.20210426152335.1"><vh>Declarations (w1_create_db.py)</vh></v>
<v t="yen.20210426152335.2"><vh>leoprint (w1_create_db.py)</vh></v>
<v t="yen.20210426152335.3"><vh>class Init(object)</vh>
<v t="yen.20210426152335.4"><vh>Init(object).__init__</vh></v>
</v>
</v>
</v>
<v t="yen.20210426151420.2"><vh>@clean w1_classroom_local_db_ready.py</vh>
<v t="yen.20210426151707.1"><vh>Declarations (w1_classroom_local_db_ready.py)</vh></v>
<v t="yen.20210426151707.2"><vh>leoprint (w1_classroom_local_db_ready.py)</vh></v>
</v>
<v t="yen.20210426153503.1"><vh>@edit w1_classroom_local_db.py</vh></v>
<v t="yen.20210426165345.1"><vh>@edit w1_classroom_local_select.py</vh></v>
</vnodes>
<tnodes>
<t tx="yen.20210426151420.2">@others
if semester == None:
    semester = '1092'
if classroomno == None:
    # BGA0810 電腦輔助設計室
    classroomno = 'BGA0810'
    
headers = {'X-Requested-With': 'XMLHttpRequest'}

url = 'https://qry.nfu.edu.tw/jclassroom_ajax.php'
post_var = {'pselyr': semester, 'pselclssroom': classroomno}

result = requests.post(url, data = post_var, headers = headers)

soup = bs4.BeautifulSoup(result.content, 'lxml')

# 先除掉所有 anchor
for a in soup.findAll('a'):
    # bs3 語法
    #a.replaceWithChildren()
    # bs4 語法, 將標註與內容拆開
    a.unwrap()

# 根據輸出設定, 取出 class='tbcls' 的 table 資料
table = soup.find('table', {'class': 'tbcls'})

# 以下要準備能夠輸入資料庫的排課時段資料 #########################
tds = [row.findAll('td') for row in table.findAll('tr')]
#leoprint(tds)
count = 0
row = 0
results = {}
for td in tds:
    row = row + 1
    for i in range(len(td)):
        if i != 0 and td[i].text != "\xa0":
            leoprint("星期"+str(i), "第"+str(row-2) + "節-", re.sub('&lt;[^&lt;]+?&gt;', '', td[i].text))
            count = count + 1
    #leoprint("***************")
leoprint("total:" + str(count))
# 以上已經取得能夠輸入資料庫的排課時段資料 ######################

# ########## 以下程式碼用來計算排課節數 ###########################
# 以下取出 td 標註資料
table_data = [i.text for i in table.find_all('td')]
#leoprint(table_data)
timeTable = []
# 去除非排課欄位資料內容
for i in table_data:
    if not "虎尾科技" in i and not "節" in i and not "\xa0" in i:
        timeTable.append(i)
#leoprint(len(timeTable))
totalNum = len(timeTable)
# ########## 以上程式碼用來計算排課節數 ##########################

# 重建 table, 設定邊線為 1 pixel
output = "總排課節數: " + str(totalNum) + "&lt;br /&gt;&lt;br /&gt;&lt;table border='1'&gt;"

for i in table.contents:
    # 利用 replace 復原 &amp;nbsp;
    output += str(i).replace("&amp;amp;nbsp", "&amp;nbsp;")
output += "&lt;/table&gt;"

#leoprint(output)

'''
# 將 output 寫入 w1_classroom.html
fileName = "w1_classroom.html"
with open(fileName, "w", encoding="utf-8") as file:
    file.write(output)
# 利用 os.system() 以 default browser 開啟 w1_class_local.html
filePath = pathlib.Path(__file__).parent.absolute()
#print(filePath)
# set firefox as default browser and start url to open html file
os.system("start file:///" + str(filePath) + "\\" + fileName)
'''
@language python
@tabwidth -4
</t>
<t tx="yen.20210426151436.1">資料表 (table) 設計:

table 名稱: course

id - 序號

semester - 排課學期

classroomno - 實驗室代號

week - 排課星期

session - 排課節次

content - 排課內容 (包含班級, 教師與課程名稱)

memo - 備註</t>
<t tx="yen.20210426151453.1"></t>
<t tx="yen.20210426151453.2">QTreeWidget {
    /* These apply to the selected item, but not to editing items.*/
    background-color: #ffffec; /* Leo's traditional tree color */
    selection-color: black; /* was white */
    selection-background-color: lightgrey;
    /* font-family: SansSerif; */
    /*font-family: DejaVu Sans Mono;*/
    font-family:YaHei Mono;
    /* 標題字型大小設定 */
    font-size: 20px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
 }

/* Headline edit widgets */
QTreeWidget QLineEdit {
    background-color: cornsilk;
    selection-color: white;
    selection-background-color: blue;
    /*font-family: DejaVu Sans Mono;*/    
    font-family:YaHei Mono;
    /* 沒有特別對應字型大小 */
    font-size: 20px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
}

/* The log panes */
QTextEdit {
    background-color: #f2fdff;
    selection-color: red;
    selection-background-color: blue;
    /* font-family: Courier New; */
    font-family:YaHei Mono;
    /* log font 大小 */
    font-size: 20px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal, italic,oblique */
}

/* The body pane */
QTextEdit#richTextEdit {
    background-color: #fdf5f5; /* A kind of pink. */
    selection-color: white;
    selection-background-color: red;
    /*font-family: DejaVu Sans Mono;*/
    /* font-family: Courier New; */
    font-family:YaHei Mono;
    /* 內文字型大小 */
    font-size: 20px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

QLabel {
    font-family:YaHei Mono;'CherryPy', 'pytz', 'mako', 'beautifulsoup4', 'pymysql', 'peewee'
    /* 下方的 Minibuffer 標題字型大小 */
    font-size: 20px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
}

/* Editor labels */
QLineEdit#editorLabel {
    background-color: #ffffec;
    font-family:YaHei Mono;
    /* 沒有直接對應字型大小 */
    font-size: 20px;
    font-weight: normal; /* normal,bold,100,..,900 */
    font-style: normal; /* normal,italic,oblique */
    border: 2px;
    margin: 2px;
}</t>
<t tx="yen.20210426151453.3">horizontal: body pane to the left
vertical: body pane on the botton</t>
<t tx="yen.20210426151707.1">import requests
import bs4
# for os.environ and os.system
import os
# for geting html file path
import pathlib
import re

# 為了讓程式能夠同時在 Leo Editor 與 SciTE 中執行列印
# 特別建立 leoprint 函式
# *args 表示 leoprint 可以接受任意數量的輸入變數
</t>
<t tx="yen.20210426151707.2">def leoprint(*args):
    try:
        g.es(*args)
    except:
        print(*args)
'''
# for pythn 3.9
proxy = 'http://[2001:288:6004:17::53]:3128'

os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy
'''
'''
url:  'jclassroom_ajax.php',
data: { pselyr: pselyr, pselclssroom: pselclssroom },
'''
semester = '1092'
classroomno = 'BGA0810'
column = True

</t>
<t tx="yen.20210426152321.1">@others
@language python
@tabwidth -4
</t>
<t tx="yen.20210426152335.1">import os
# sqlite3 模組為 Python3 內建
import sqlite3
 

</t>
<t tx="yen.20210426152335.2"># 為了讓程式能夠同時在 Leo Editor 與 SciTE 中執行列印
# 特別建立 leoprint 函式
# *args 表示 leoprint 可以接受任意數量的輸入變數
def leoprint(*args):
    try:
        g.es(*args)
    except:
        print(*args)
 
# 資料庫檔案將與程式放在同一目錄
data_dir = "./"
 
</t>
<t tx="yen.20210426152335.3">class Init(object):
    @others
# 建立案例
init = Init()
leoprint("done")
</t>
<t tx="yen.20210426152335.4">def __init__(self):
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
 
</t>
<t tx="yen.20210426152501.1"></t>
</tnodes>
</leo_file>
