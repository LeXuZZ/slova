# coding=utf-8
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/get_dictionary')
def get_dictionary():
    words_list = ['ЗАЛ', 'ВЕС', 'ЗУБ']
    return words_list

@app.route('/')
def main_page():
    return render_template('test.html')


if __name__ == '__main__':
    app.run()
