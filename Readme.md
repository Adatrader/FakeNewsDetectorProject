# Fake News Detector Rest API/Web App

Deployed here: https://fakenewsurldetector.herokuapp.com/  
API Documentation: <a href="doc:introduction" target="https://documenter.getpostman.com/view/13246655/TVYGbcxp?">Postman API Examples for Twitter/Facebook</a>

## Run Locally

<br/>

Running on http://127.0.0.1  
Port: 5000  
to view front end and access api

```
pip3 install Flask nltk newspaper3 bs4 requests
Debug = True
app.run()
```

## Run On Heroku

<br/>
Files needed:
Procfile, requirements, runtime, app.py, templates, and static files<br/>

<br/>Stage Files<br/>

```
cd [location]
Open git bash
git init .
git add app.py Procfile requirements.txt runtime.txt
git commit -m 'Changes_that_occured'
git push heroku master
```

<br/> Set up Heroku<br/>

```
heroku login -i
heroku git:remote -a {your-project-name}
git push heroku master

To see logs:
heroku logs --tail
```

Live Version:<br/>

```
Debug = False
#app.run()
```
