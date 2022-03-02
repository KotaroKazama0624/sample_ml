from flask import Flask, render_template, redirect
from flask import request, jsonify
import pandas as pd
import pickle


app = Flask(__name__)

#機械学習モデルの読み込み
model_file_name='stockmodel.pkl'
model = pickle.load(open(model_file_name, 'rb'))

#URLの指定
@app.route('/')
def index():
    return render_template('index.html')

#index.htmlのformから受け取った時の処理
@app.route('/kabuka', methods=['POST'])
def lower_conversion():
    monday = request.form['monday']
    tuesday = request.form['tuesday']
    wednesday = request.form['wednesday']
    thursday = request.form['thursday']
    #受け取ったデータをデータフレームに変換
    df = pd.DataFrame({'monday':[monday], 
                       'tuesday':[tuesday],
                       'wednesday':[wednesday],
                       'thursday':[thursday],})
    #予測
    result = model.predict(df)
    #予測結果をint型に変更
    result = result.item()
    rank = ''
    if result == 1:
        rank = '上がる'
    else:
        rank = '下がる'

    #index.htmlに変更内容を送る
    return render_template('index.html', rank = rank)

if __name__ == '__main__':
    app.run()