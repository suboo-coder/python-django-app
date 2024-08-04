# python-django-app

## Stpes
- pip install -r requirements.txt

- django-admin startproject stocks

### To run server
- cd stocks

- python manage.py runserver

### To migrate db
- python manage.py migrate

- python manage.py createsuperuser


### Create App quotes
- python manage.py startapp quotes
- Each app needs to have it urls file. Create quotes/urls.py

### Run Migrations
- Create Migrations
python manage.py makemigrations
- Push Migration to DB
python manage.py migrate


### References
- [Bootstrap](https://getbootstrap.com/docs/5.2/getting-started/introduction/)
- [Metalpriceapi](https://metalpriceapi.com/dashboard)
- [AlphaVantage](https://www.alphavantage.co/documentation/)
