#-*-coding: utf-8-*-
# 创建时间: 2020/9/5 15:22

from flask import request, Flask, jsonify
from config import *
from parse_html import parse_html_zh2en
from google_translate import translate_list_data,translate_data


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/', methods=['GET'])
def index():
    return "hello world",201


@app.route('/html/en', methods=['POST'])
def post_Data():
    wp_content = request.form['wp_content']
    translate_wp_content = parse_html_zh2en(wp_content)
    recognize_info = {'wp_content': translate_wp_content}
    return jsonify(recognize_info), 201


@app.route('/translate/<id>', methods=['POST'])
def post_translate_data(id):
    wp_content = request.form['wp_content']
    translate_wp_content = translate_data(id,wp_content)
    recognize_info = {'wp_content': translate_wp_content}
    return jsonify(recognize_info), 201


@app.route('/translate_list/<id>', methods=['POST'])
def post_translate_data_list(id):
    wp_content = request.form['wp_content']
    translate_wp_content = translate_list_data(id,wp_content)
    recognize_info = {'wp_content': translate_wp_content}
    return jsonify(recognize_info), 201


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000,threaded=True)