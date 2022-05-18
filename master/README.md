# Holons
Holons is based on Django and Postgres, so you ought to have Python 3, pip3, virtual environments and Postgres installed and working.Frontend is based on Vue.js, so get npm ready.



## Local setup

### Database
Create Postgres database called holons

Get the sourcecode

```
cd ~/work/holons
git clone  .
```

Check ~/work/holons/website/holons/development_settings.py for database connection settings

Set up virtual environment

```
cd website
python3 -m venv venv && cd holons && pip3 install -r requirements.txt && cd - && source ./setenv.sh
```
./setenv.sh starts venv and makes Django use local settings file (development_settings.py), not production (settings.py)

Check if it works

```
cd ~/work/holons/website/holons/
./manage.py
```

Migrate database

```
cd ~/work/holons/website/holons/ && ./manage.py migrate
```

Install nodejs  modules

### @todo
Basic layout is build via gulp from /src directory
```
cd ~/work/holons/src/
npm install
npm install gulp -g
gulp build
```


```
cd ~/work/holons/website/holons-front
npm install
```

Build vue.js part of the app, collect static and run a local development server

```
cd ~/work/holons/website/holons
cd ../holons-front && npm run build && cd ../holons && ./manage.py collectstatic --noinput && ./manage.py runserver
```

Go to http://localhost:8000 and look at what you've done
