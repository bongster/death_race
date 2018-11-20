# Death race

> This is for leaderboard site for crossfit games name Death race

heroku setting

```
git remote add heroku https://git.heroku.com/secure-lowlands-80109.git
```


## dump data from heroku

```
heroku run python manage.py dumpdata --natural-foreign -- > data.json
```

## Load data to local

```
python3 manage.py loaddata data.json
```