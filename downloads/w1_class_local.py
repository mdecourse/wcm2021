import requests
import bs4
# for os.environ and os.system()
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
url:  'class_ajax.php',
data: { pselyr: pselyr, pselclss: pselclss
'''
semester = '1092'
classno = '42311'
column = True

if semester == None:
    semester = '1091'
if classno == None:
    # 42311 is 設一甲
    classno = '42311'
    
headers = {'X-Requested-With': 'XMLHttpRequest'}

url = 'https://qry.nfu.edu.tw/class_ajax.php'
post_var = {'pselyr': semester, 'pselclss': classno}

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

# 重建 table, 設定邊線為 1 pixel
output = "<table border='1'>"

for i in table.contents:
    # 利用 replace 復原 &nbsp;
    output += str(i).replace("&amp;nbsp", "&nbsp;")
output += "</table>"
# print(output)
# 將 output 寫入 w1_class_local.html
with open("w1_class_local.html", "w", encoding="utf-8") as file:
    file.write(output)
# 利用 os.system() 以 default browser 開啟 w1_class_local.html
filePath = pathlib.Path(__file__).parent.absolute()
#print(filePath)
# set firefox as default browser and start url to open html file
os.system("start file:///" + str(filePath) + "\\w1_class_local.html")
