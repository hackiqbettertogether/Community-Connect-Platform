from flask import Flask,request
from flask_restful import Api,Resource,reqparse
import nltk
import string
import re
from nltk.sentiment import SentimentIntensityAnalyzer
from warnings import filterwarnings
import pandas as pd
dataFrame = pd.read_excel("gender_inclusive.xlsx")
dataFrame['less_inclusive'] = dataFrame['less_inclusive'].apply(lambda x:x.lower())
dataFrame['more_inclusive'] = dataFrame['more_inclusive'].apply(lambda x:x.lower())
dataFrame['purpose'] = dataFrame['purpose'].apply(lambda x:x.lower())
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
        return {"score":sentiment_analyser(comment) + inclusion_calculator(comment)}


def remove_punctuation(text):
    punctuationfree="".join([i.lower() for i in text if i not in string.punctuation])
    numberfree = re.sub(r'[0-9]+', '', punctuationfree)
    return numberfree
def sentiment_analyser(comment):
    total = 10
    sia = SentimentIntensityAnalyzer()
    text = remove_punctuation(comment)
    result = sia.polarity_scores(text)
    if result['neg']>result['pos']:
        total = 2
    elif result['pos']>result['neg']:
        total = 10
    if result['neu']>0.5:
        total = total-2
    return total

def inclusion_calculator(comment):
    total = 10
    words = [i.lower() for i in comment.split(" ")]
    less_inclusive_words = [word for word in words if word in dataFrame['less_inclusive'].values]
    more_inclusive_words = [word for word in words if word in dataFrame['more_inclusive'].values]
    less_counts = len(less_inclusive_words)
    more_count = len(more_inclusive_words)
    negative = less_counts/len(words)
    positive = more_count/len(words)
    if negative>positive:
        total = total-7
    elif negative<positive:
        total = 10
    elif negative == positive:
        total = 5
    return total

api.add_resource(SentimentScore,"/sentiment-score")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5001)