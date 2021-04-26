import requests
import bs4
# for os.environ and os.system
import os
# for geting html file path
import pathlib

# for pythn 3.9
proxy = 'http://[2001:288:6004:17::69]:3128'

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

# ########## 以下程式碼用來計算排課節數 ##########
# 以下取出 td 標註資料
table_data = [i.text for i in table.find_all('td')]
#print(table_data)
timeTable = []
# 去除非排課欄位資料內容
for i in table_data:
    if not "虎尾科技" in i and not "節" in i and not "\xa0" in i:
        timeTable.append(i)
#print(len(timeTable))
totalNum = len(timeTable)
# ########## 以上程式碼用來計算排課節數 ##########

# 重建 table, 設定邊線為 1 pixel
output = "總排課節數: " + str(totalNum) + "<br /><br /><table border='1'>"

for i in table.contents:
    # 利用 replace 復原 &nbsp;
    output += str(i).replace("&amp;nbsp", "&nbsp;")
output += "</table>"
#print(output)

# 將 output 寫入 w1_classroom.html
fileName = "w1_classroom.html"
with open(fileName, "w", encoding="utf-8") as file:
    file.write(output)
# 利用 os.system() 以 default browser 開啟 w1_class_local.html
filePath = pathlib.Path(__file__).parent.absolute()
#print(filePath)
# set firefox as default browser and start url to open html file
os.system("start file:///" + str(filePath) + "\\" + fileName)
