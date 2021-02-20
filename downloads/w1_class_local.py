import requests
import bs4

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
    a.replaceWithChildren()

# 根據輸出設定, 取出 class='tbcls' 的 table 資料
table = soup.find('table', {'class': 'tbcls'})

# 重建 table, 設定邊線為 1 pixel
output = "<table border='1'>"

for i in table.contents:
    # 利用 replace 復原 &nbsp
    output += str(i).replace("&amp;nbsp", "&nbsp")
output += "</table>"
print(output)
