import requests

r = requests.get("https://mde.tw")
print("status_code:", r.status_code)
print("content-type:", r.headers['content-type'])
print("encoding:", r.encoding)
#print("text:", r.text)
print("content:", r.content)
