from flask import Flask
from tweet import tweet_api
import os

app = Flask(__name__)
app.register_blueprint(tweet_api, url_prefix = '/')

if __name__ == ('__main__'):
    app.run(debug=True, port=os.getenv('PORT'), host=os.getenv('HOST'))