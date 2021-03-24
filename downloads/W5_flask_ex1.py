from flask import Flask, request
from datetime import datetime
import os

# for pythn 3.9
proxy = 'http://[2001:288:6004:17::69]:3128'
''' 
os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy
'''
app = Flask(__name__)

# https://realpython.com/primer-on-python-decorators/
@app.route('/')
def hello():
    # 若取不到 name 則 name = None
    name = request.args.get('name')
    if name == None:
        name = "test"
    # https://realpython.com/python-formatted-output/
    return HELLO_HTML.format(
            name, str(datetime.now()))

HELLO_HTML = """
    <html><body>
        <h1>Hello, {0}!</h1>
        現在時間為: {1}.
    </body></html>"""

if __name__ == "__main__":
    # Launch the Flask dev server
    app.run(host="localhost", debug=True)