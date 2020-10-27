# pip3 install newspaper3k
from newspaper import Article
import nltk
import flask
from flask import request, jsonify
nltk.download('punkt')


# Debug allows for changes to be seen in real time.
app = flask.Flask(__name__)
app.config["DEBUG"] = True

#Place holder for landing page for webscraper
@app.route('/api/v1/', methods=['GET'])
def homePage():
    return '''
    <h1>News Site WebScraper API</h1>
    <h3>You are at: /home/</h3>
    <p>To submit a new url to database: POST '/api/v1/?url=url.com'
    <p>To view all submitted urls in the database: '/api/v1/newsurl/all' </p>
    <p>To get metadata based on news url id : '/api/v1/newsurl/?id=xxxxxx' </p>
'''

# Catch 404 errors
@app.errorhandler(404)
def pageNotFound(e):
    return "<h1>Error 404:</h1><p>Page not found.</p>", 404

# Get all the urls in database
@app.route('/api/v1/newsurl/all', methods=['GET'])
def getAll():
    
    
    return 0
    
# Get json of url in database
@app.route('/api/v1/newsurl/', methods=['GET'])
def getId():
    
    
    return 0
    

# Submit new url for webscraping 
@app.route('/api/v1/', methods=['POST'])
def newEntry():
    urlPassed = request.args.get('url')
    obj = newsUrl(urlPassed)
    objDict = obj.createJSON(obj.url)

    return objDict


class newsUrl:
    def __init__(self, urlGiven):
        self.url = urlGiven

    def createJSON(self, url):
        
        # Metadata
        article = self.parseUrl(self.url)
        author = self.getAuthor(article)

        #Encoding for json string is adding the \u, \t, \n etc 
        # shouldn't cause issues when recieved and decoded -> print(text) here to show
        text = self.getText(article)

        date = self.getDate(article)
        title = self.getTitle(article)
        
        # NLP info
        summary = self.getSummary(article)
        keywords = self.getKeywords(article)
        
        # Create dictionary
        tempDict = {
        'url': url,
        'title': title,
        'publish_date': str(date), 
        'authors': author,
        'summary': summary,
        'keywords': keywords, 
        'content': text
        }
        return jsonify(tempDict)

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


# Comment out for deployment
# app.run()
