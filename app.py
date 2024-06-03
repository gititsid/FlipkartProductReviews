import sys
import requests
import pymongo

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq


from src.get_reviews import FlipkartProductReviews
from src.logger import logging
from src.exception import CustomException

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
        try:
            search_item = request.form['content'].replace(" ", "")
            number_of_reviews = 10

            flipkart_review_scrapper = FlipkartProductReviews()
            reviews = flipkart_review_scrapper.get_review_details(search_item, number_of_reviews)

            return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])
        
        except Exception as e:
            logging.info(e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

