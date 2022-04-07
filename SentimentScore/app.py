from flask import Flask,request
from flask_restful import Api,Resource,reqparse
import nltk
import string
import re
from nltk.sentiment import SentimentIntensityAnalyzer
from warnings import filterwarnings
filterwarnings("ignore")


nltk.download('vader_lexicon')

#defining the function to remove punctuation



app= Flask(__name__)
api=Api(app)

parser = reqparse.RequestParser()
parser.add_argument('comment', type=str)


class SentimentScore(Resource):
    def post(self):
        request.get_json(force=True)
        args = parser.parse_args()
        comment = str(args['comment'])
        return {"score":sentiment_analyser(comment)}


def remove_punctuation(text):
    punctuationfree="".join([i.lower() for i in text if i not in string.punctuation])
    numberfree = re.sub(r'[0-9]+', '', punctuationfree)
    return numberfree
def sentiment_analyser(comment):
    total=0
    sia = SentimentIntensityAnalyzer()
    text = remove_punctuation(comment)
    result = sia.polarity_scores(text)
    if result['neg']>result['pos']:
        total = -5
    elif result['pos']>result['neg']:
        total = 10
    if result['neu']>0.5:
        total = 0
    return total

api.add_resource(SentimentScore,"/sentiment_score")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5001)