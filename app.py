# pip3 install newspaper3k
from newspaper import Article
import newspaper
import nltk
import flask
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, render_template
import json
# To make requests
import requests
nltk.download('punkt')  # TODO: Uncomment during local testing

# Debug allows for changes to be seen in real time.
app = flask.Flask(__name__)
app.config["DEBUG"] = True  # TODO: Set to True for local testing


@app.route('/')
def index():
    return render_template('index.html')

# Unused now (Directs to postman)


@app.route('/api/v1/readthedocs')
def readthedocs():
    return render_template('readthedocs.html')


# Catch 404 errors
@app.errorhandler(404)
def pageNotFound(e):
    return "<h1>Error 404:</h1><p>Page not found.</p>", 404


# For front end results page
@app.route('/results', methods=['POST'])
def results():
    if request.method == 'POST':
        urlPassed = request.form['url_submit']

        if urlPassed == '':
            return render_template('index.html', message='Please enter required field')
    origin = "WebApp"  # Specify Web App origin for KB team
    obj = newsUrl(urlPassed, origin)
    # Returned dictionary from scraper
    dictObj = obj.createJSON(obj.url, obj.origin)
    jsonGenerated = jsonify(dictObj)  # Send to NN/KB Team
    # print(dictObj)
    # TODO: Sent to NN team (get response with confidence score)
    headr = {'content-type': 'application/json', 'accept': '*/*'}
    returnedNN = requests.post(
        url='https://viksri.com/fakenewsproj/api', data=json.dumps(dictObj), headers=headr)
    responseScore = returnedNN.json()
    frontResult = "FAKE"
    if responseScore['score'] == 1:
        frontResult = "REAL"

    return render_template('result.html', urlTitle=dictObj.get('url'),
                           conf=frontResult, result=dictObj.get('page_data'))


@app.route('/api/v1/twitter', methods=['POST'])
def twitter():
    content = request.get_json()
    if content == None:
        return {"response": "400 Bad Request"}
    urlGiven = content['url']
    origin = "Twitter"  # Specify Twitter origin for KB team
    obj = newsUrl(urlGiven, origin)
    # Returned dictionary from scraper
    dictObj = obj.createJSON(obj.url, obj.origin)
    combinedObj = Merge(content, dictObj)
    jsonGenerated = jsonify(combinedObj)
    # TODO: Sent to NN team (get response with confidence score)
    headr = {'content-type': 'application/json', 'accept': '*/*'}
    returnedNN = requests.post(
        url='https://viksri.com/fakenewsproj/api', data=json.dumps(dictObj), headers=headr)
    responseScore = returnedNN.json()

    # Reformat for Json Response
    dictObj['confidence_score'] = responseScore['score']
    tempDict = dictObj['page_data']
    # Switch back to content
    tempDict['content'] = tempDict['body']
    del tempDict['body']
    # Swtich publish date
    tempDict['publish_date'] = tempDict['publish_date_time']
    del tempDict['publish_date_time']
    # Switch publisher
    tempDict['site_name'] = tempDict['publisher']
    del tempDict['publisher']
    dictObj['url_info'] = tempDict
    del dictObj['page_data']

    # Merge response
    combinedObj = Merge(content, dictObj)
    jsonGenerated = jsonify(combinedObj)
    return jsonGenerated


@app.route('/api/v1/facebook', methods=['POST'])
def facebook():
    content = request.get_json()
    if content == None:
        return {"response": "400 Bad Request"}
    urlGiven = content['url']
    origin = "Facebook"  # Specify Facebook origin for KB team
    obj = newsUrl(urlGiven, origin)
    # Returned dictionary from scraper
    dictObj = obj.createJSON(obj.url, obj.origin)
    # TODO: Sent to NN team (get response with confidence score)
    headr = {'content-type': 'application/json', 'accept': '*/*'}
    returnedNN = requests.post(
        url='https://viksri.com/fakenewsproj/api', data=json.dumps(dictObj), headers=headr)
    responseScore = returnedNN.json()

    # Reformat for Json Response
    dictObj['confidence_score'] = responseScore['score']
    tempDict = dictObj['page_data']
    # Switch back to content
    tempDict['content'] = tempDict['body']
    del tempDict['body']
    # Swtich publish date
    tempDict['publish_date'] = tempDict['publish_date_time']
    del tempDict['publish_date_time']
    # Switch publisher
    tempDict['site_name'] = tempDict['publisher']
    del tempDict['publisher']
    dictObj['url_info'] = tempDict
    del dictObj['page_data']

    # Merge response
    combinedObj = Merge(content, dictObj)
    jsonGenerated = jsonify(combinedObj)
    return jsonGenerated


# Merge two dictionaries
def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res


class newsUrl:
    def __init__(self, urlGiven, origin):
        self.url = urlGiven
        self.origin = origin

    def createJSON(self, url, origin):

        # Get title, subtitle, and citation urls
        titleCitationObj = newspaper.build(self.url)
        siteName = self.getSiteName(titleCitationObj)
        subtitle = self.getSubtitle(titleCitationObj)
        # Metadata
        try:
            article = self.parseUrl(self.url)
        except:
            totalDict = {'url': url}
            totalDict['origin'] = origin
            totalDict['confidence_score'] = 0.5
            totalDict['page_data'] = "Unable to Parse"
            return totalDict
        author = self.getAuthor(article)
        citUrl = self.getCitationUrls(article)

        # Encoding for json string is adding the \u, \t, \n etc
        # shouldn't cause issues when recieved and decoded -> print(text) here to show
        text = self.getText(article)

        date = self.getDate(article)
        title = self.getTitle(article)
        # siteName = self.getSiteName(Article(self.url))
        # NLP info
        summary = self.getSummary(article)
        keywords = self.getKeywords(article)

        # Create dictionary
        totalDict = {'url': url}
        totalDict['origin'] = origin
        totalDict['confidence_score'] = 0.5
        tempDict = {
            'title': title,
            'publisher': str(siteName),
            'subtitle': str(subtitle),
            'publish_date_time': str(date),
            'authors': author,
            'natural_language_processing': {
                'summary': summary,
                'keywords': keywords
            },
            'body': text,
            'citation_urls': citUrl
        }
        totalDict['page_data'] = tempDict

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

    # Site Name
    def getSiteName(self, newspaper):
        return newspaper.brand

    # Site Description
    def getSubtitle(self, newspaper):
        return newspaper.description

    # Citation Urls
    def getCitationUrls(self, article):
        urlsArr = []
        soup = BeautifulSoup(article.html, 'html.parser')
        for link in soup.find_all('a'):
            linkTemp = link.get('href')
            # Breitbart style pages fix
            if linkTemp != None:
                if linkTemp.startswith('http'):
                    urlsArr.append(linkTemp)
        return urlsArr

    # Natural language processing to generate summary and keywords from article
    # Keywords
    def getKeywords(self, article):
        article.nlp()
        return article.keywords

    def getSummary(self, article):
        article.nlp()
        return article.summary


app.run()
