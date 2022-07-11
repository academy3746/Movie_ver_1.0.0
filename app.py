from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup


from pymongo import MongoClient
client = MongoClient('mongodb+srv://admin:1q2w3e4r!@cluster0.n5ejj.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')


# Required Variable
# 1. url
# 2. star
# 3. comment

@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    # Start Web Crawling
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one('meta[property="og:title"]')['content']
    image = soup.select_one('meta[property="og:image"]')['content']
    desc = soup.select_one('meta[property="og:description"]')['content']

    # INSERT INTO MOVIES('TITLE','IMAGE','DESC','STAR','CONTENT') VALUE(?,?,?,?,?)
    doc = {
        'title':title,
        'image':image,
        'desc':desc,
        'star':star_receive,
        'comment':comment_receive
    }
    db.movies.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})


@app.route("/movie", methods=["GET"])
def movie_get():
    # SELECT * FROM MOVIES
    movie_list = list(db.movies.find({}, {'_id': False}))

    # Return Movie List Array to ajax
    return jsonify({'movies': movie_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
