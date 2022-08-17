Requirements: before pulling the project install python 3.8

**Installation:**
1. Pull the project from repo
2. In your terminal create virtual env -> run command in your terminal: python3 -m venv env
3. Enter your venv -> you should be in the directory where your venv is located: source env/bin/activate
4. Run the following command in your terminal -> pip3 install requirements.txt
5. Create local db in postgres or use creds for existing one
6. After all packages are installed create .env file in backend folder and add env variables:
    - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; SECRET_KEY=YOUR_SECRET - to generate one you can use https://djecrety.ir
    - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; DB_NAME=NAME_OF_YOUR_DB
    - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; DB_USER=DB_USER
    - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; DB_PASSWORD=DB_PASS
    - &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; DB_HOST=DB_HOST
7. In your terminal run -> ./manage.py migrate
8. Create superuser via termianl -> ./manage.py createsuperuser

To run local server use the following command in the terminal -> ./manage.py runserver
