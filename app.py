from flask import Flask, request, jsonify
import requests
import os
import pandas as pd

app = Flask(__name__)

API_KEY = os.getenv('RAKUTEN_API_KEY')  # 環境変数からAPIキーを取得
url = 'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601'

@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword', '')
    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400
    try:
        items = search_items(keyword)
        return jsonify({'success': True, 'data': items})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

def search_items(keyword, pages=10):
    all_items = []
    for page in range(1, pages + 1):
        params = {
            'applicationId': API_KEY,
            'format': 'json',
            'keyword': keyword,
            'sort': '+itemPrice',
            'hits': 30,
            'page': page
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception('API request failed with status code ' + str(response.status_code))
        data = response.json()
        items = data['Items']
        item_list = [{'商品名': item['Item']['itemName'], '価格': item['Item']['itemPrice']} for item in items]
        all_items.extend(item_list)
        if len(items) < 30:
            break
    return all_items

if __name__ == '__main__':
    app.run(debug=True)