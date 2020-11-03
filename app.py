# pip3 install newspaper3k
from newspaper import Article
import nltk
import flask
from flask import Flask, request, jsonify, render_template
# To make requests
import requests
nltk.download('punkt') #TODO: Uncomment during deployment

# Debug allows for changes to be seen in real time.
app = flask.Flask(__name__)
app.config["DEBUG"] = False  # TODO: Set to false during deployment


@app.route('/')
def index():
    # f = open('home.html')
    return render_template('index.html')

# Unused now (Directs to postman)


@app.route('/api/v1/readthedocs')
def readthedocs():
    return render_template('readthedocs.html')


# Catch 404 errors
@app.errorhandler(404)
def pageNotFound(e):
    return "<h1>Error 404:</h1><p>Page not found.</p>", 404

# use beautiful soup for KB team
# url - get href tags (excluding root domains)
# pass along all twitter

# add origin as an attribute in json
# Twitter
#       POST {id}
#             addition attributes from twitter + url
#             response: 200 Submitted
#       GET {id}
#             response: JSON with confidence score and parsed information
#       GET {all}
#             response: JSON array with all id's in sql database
#       DELETE {id}
#             response: deleted
# Facebook
#       POST {id}
#             addition attributes from facebook + url
#             response: 200 Submitted
#       GET {id}
#             response: JSON with confidence score and parsed information
#       GET {all}
#             response: JSON array with all id's in sql database
#       DELETE {id}
#             response: deleted
# Web App
#        POST {id}
#             response: 200 Submitted
#       GET {id}
#             response: JSON with confidence score and parsed information
#       GET {all}
#             response: JSON array with all id's in sql database
#       DELETE {id}
#             response: deleted

# Get all the urls in database


@app.route('/api/v1/newsurl/all', methods=['GET'])
def getAll():

    return 0

# Get json of url in database


@app.route('/api/v1/newsurl/', methods=['GET'])
def getId():

    return 0

# TODO: Last working before testing new endpoints
# # Submit new url for webscraping
# @app.route('/api/v1/webapp/', methods=['POST'])
# def newEntry():
#     urlPassed = request.args.get('url')
#     obj = newsUrl(urlPassed)
#     jsonObj = obj.createJSON(obj.url)
#     # Sent to NN team (get response with confidence score)
#     # confidenceScore = requests.post(url = 'www.yourNNServer.com', data=jsonObj)
#     return jsonObj


# For front end results page
@app.route('/results', methods=['POST'])
def results():
    if request.method == 'POST':
        urlPassed = request.form['url_submit']

        if urlPassed == '':
            return render_template('index.html', message='Please enter required field')
    origin = "WebApp"
    obj = newsUrl(urlPassed, origin)
    # Returned dictionary from scraper
    dictObj = obj.createJSON(obj.url, obj.origin)
    jsonGenerated = jsonify(dictObj)  # Send to NN/KB Team
    print(dictObj)
    # TODO: Sent to NN team (get response with confidence score)
    # confidenceScore = requests.post(url = 'www.yourNNServer.com', data=jsonObj)

    return render_template('result.html', urlTitle=dictObj.get('url'),
                           conf=dictObj.get('confidence_score'), result=dictObj.get('url_info'))

# Submit new url for webscraping


@app.route('/api/v1/twitter', methods=['POST'])
def twitter():
    content = request.get_json()
    if content == None:
        return {"response": "400 Bad Request"}
    urlGiven = content['url']
    origin = "Twitter"
    obj = newsUrl(urlGiven, origin)
    # Returned dictionary from scraper
    dictObj = obj.createJSON(obj.url, obj.origin)
    combinedObj = Merge(content, dictObj)
    jsonGenerated = jsonify(combinedObj)  # Send to NN/KB Team
    # TODO: Sent to NN team (get response with confidence score)
    # confidenceScore = requests.post(url = 'www.yourNNServer.com', data=jsonObj)
    return jsonify(combinedObj)


@app.route('/api/v1/facebook', methods=['POST'])
def facebook():
    content = request.get_json()
    if content == None:
        return {"response": "400 Bad Request"}
    urlGiven = content['url']
    origin = "Facebook"
    obj = newsUrl(urlGiven, origin)
    # Returned dictionary from scraper
    dictObj = obj.createJSON(obj.url, obj.origin)
    combinedObj = Merge(content, dictObj)
    jsonGenerated = jsonify(combinedObj)  # Send to NN/KB Team
    # TODO: Sent to NN team (get response with confidence score)
    # confidenceScore = requests.post(url = 'www.yourNNServer.com', data=jsonObj)

    return jsonify(combinedObj)


# Merge two dictionaries
def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res


class newsUrl:
    def __init__(self, urlGiven, origin):
        self.url = urlGiven
        self.origin = origin

    def createJSON(self, url, origin):

        # Metadata
        article = self.parseUrl(self.url)
        author = self.getAuthor(article)

        # Encoding for json string is adding the \u, \t, \n etc
        # shouldn't cause issues when recieved and decoded -> print(text) here to show
        text = self.getText(article)

        date = self.getDate(article)
        title = self.getTitle(article)

        # NLP info
        summary = self.getSummary(article)
        keywords = self.getKeywords(article)

        # Create dictionary
        totalDict = {'url': url}
        totalDict['origin'] = origin
        totalDict['confidence_score'] = 0
        tempDict = {
            'title': title,
            'publish_date': str(date),
            'authors': author,
            'summary': summary,
            'keywords': keywords,
            'content': text
        }
        totalDict['url_info'] = tempDict

        return totalDict
        # return jsonify(tempDict)

    def parseUrl(self, url):
        article = Article(self.url)
        article.download()
        article.html
        article.parse()
        return article

    # Author
    def getAuthor(self, article):
        auth = article.authors
        print(len(auth))
        for x in auth:
            count = 0
            for char in x:
                if (char == ' '):
                    count += 1
            if(count > 3):
                auth.remove(x)
        return auth

    # Content
    def getText(self, article):
        return article.text

    # Date
    def getDate(self, article):
        return article.publish_date

    # Title
    def getTitle(self, article):
        return article.title

    def getSiteName(self, article):
        return article.site

    # Natural language processing to generate summary and keywords from article
    # Keywords
    def getKeywords(self, article):
        article.nlp()
        return article.keywords

    def getSummary(self, article):
        article.nlp()
        return article.summary

