# Fake News Detector Rest API/Web App

Deployed here: https://fakenewsurldetector.herokuapp.com/  
API Documentation: https://documenter.getpostman.com/view/13246655/TVYGbcxp?

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
heroku login -i
heroku git:remote -a {your-project-name}
```

<br/> Push to Heroku<br/>

```
git add .
git commit -m 'Changes_that_occured'
git push heroku master

To see logs:
heroku logs --tail
```

Live Version:<br/>

```
Debug = False
#app.run()
```
