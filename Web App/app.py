from flask import Flask, render_template, request, redirect, abort, jsonify, make_response
from werkzeug.utils import secure_filename
from retrieval import *
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


# For GPU Configure
from spleeter.separator import Separator
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

df = pd.read_csv('static/lyrics_data.csv',encoding='utf8')

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def main():

    global classes
    global tfidf_vect_ngram
    global data_tfidf_ngram

    # Buoc 1: Load data
    data, classes = load_data_in_a_directory('./static/data/*.txt')
    print('Total database: {}'.format(len(data)))

    # Buoc 2 tinh' TF_IDF kết hợp 2 từ liên tiếp nhau
    tfidf_vect_ngram = TfidfVectorizer(analyzer='word', max_features=5000, ngram_range=(2, 3))
    tfidf_vect_ngram.fit(data)
    data_tfidf_ngram = tfidf_vect_ngram.transform(data)

    return render_template('public/index.html')

@app.route('/retrieval', methods = ['POST'])
def search():

    req = request.files['file'].read()

    rank = run(req,data_tfidf_ngram,tfidf_vect_ngram, classes)
    Title = []
    Singer = []
    Img = []
    Song = []
    Link = []

    for x in rank:
        temp = df[df.Title == x]
        for y in temp.Title:
            Title.append(y)
        for y in temp.Singer:
            Singer.append(y)
        for y in temp.Img:
            Img.append(y)
        for y in temp.Link:
            Link.append(y)
        for y in temp.Mp3:
            Song.append(y)

    f = open("static/data/" + Title[0] +".txt", "r", encoding='utf8')
    lyric = [x.replace('\n',' <br> ') for x in f.readlines()]

    print(rank)
    # print(Title,Singer,Img,Song,Link)

    message = {"Title": Title[:4],"Singer": Singer[:4],"Image": Img[:4],"Song": Song[:2], "URL": Link[:4], "Lyrics": lyric}

    res = make_response(jsonify({"message":message}), 200)
    return res





if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
    app.run(debug=True)
