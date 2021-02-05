#-*-coding: utf-8-*-
# 创建时间: 2020/9/5 15:22

from flask import request, Flask, jsonify
from api_img import *


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/', methods=['GET'])
def index():
    return "hello world",201


@app.route('/img', methods=['POST'])
def post_return_web_url():
    web_url = request.form['web_url']
    return_web_url = request_download(web_url)
    recognize_info = {'return_web_url': return_web_url}
    return jsonify(recognize_info), 201


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=6666,threaded=True)