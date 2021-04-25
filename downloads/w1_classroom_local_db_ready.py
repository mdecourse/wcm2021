import requests
import bs4
# for os.environ and os.system
import os
# for geting html file path
import pathlib
import re

# 為了讓程式能夠同時在 Leo Editor 與 SciTE 中執行列印
# 特別建立 leoprint 函式
# *args 表示 leoprint 可以接受任意數量的輸入變數
def leoprint(*args):
    try:
        g.es(*args)
    except:
        print(*args)

# for pythn 3.9
proxy = 'http://[2001:288:6004:17::53]:3128'

os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

'''
url:  'jclassroom_ajax.php',
data: { pselyr: pselyr, pselclssroom: pselclssroom },
'''
semester = '1092'
classroomno = 'BGA0810'
column = True

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
            leoprint("星期"+str(i), "第"+str(row-2) + "節-", re.sub('<[^<]+?>', '', td[i].text))
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
output = "總排課節數: " + str(totalNum) + "<br /><br /><table border='1'>"

for i in table.contents:
    # 利用 replace 復原 &nbsp;
    output += str(i).replace("&amp;nbsp", "&nbsp;")
output += "</table>"

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