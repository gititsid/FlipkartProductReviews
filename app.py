import sys
from flask import Flask, render_template, request
from src.utils.common_utils import save_to_csv, push_to_mongodb
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
            number_of_reviews = 50

            flipkart_review_scrapper = FlipkartProductReviews()
            reviews = flipkart_review_scrapper.get_review_details(search_item, number_of_reviews)

            save_to_csv(reviews, filename=search_item)
            push_to_mongodb(reviews=reviews)

            return render_template('result.html', reviews=reviews)
        
        except Exception as e:
            logging.error("Error occured on /review route!")
            raise CustomException(e, sys)
    else:
        return render_template('index.html')
    
    
if __name__=="__main__":
    app.run(host="0.0.0.0", port=8000)

