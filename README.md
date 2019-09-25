## Currency Service API

### Local deploy
1. Configure enviroment
    ```
    python3 -m venv env
    ```
2. Install requirements
    ```
    pip install -r requirements.txt 
    ``` 
3. Apply migrations
    ```
    python manage.py migrate
    ```
4. Create superuser
    ```
    python manage.py creattesuperuser
    ```
5. Run server
    ```
    python manage.py runserver
    ```
    
### Heroku deploy
1. Create app
    ```
    heroku create
    ```
2. Push to heroku
    ```
    git push heroku master
    ```
3. Create superuser
    ```
    heroku run python manage.py createsuperuser
    ```
4. Open heroku
    ```
    heroku open
    ```