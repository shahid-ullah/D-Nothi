### Server installation Instructions

1. clone the project
2. cd D-Nothi
3. create virtual environment and active virtual environment
  1. $ virtualenv venv
  2. $ source venv/bin/activate
4. Install project dependencies
  1. pip install -r requirements.txt
5. collect static files
  1. python manage.py collectstatic
5. Start development server
  1. python manager.py runserver


### Additional Instructions
-  create .env file in project root directory and put required value
    ```
  SECRET_KEY=''
  DEBUG=False
  DB_NAME=''
  DB_USER=''
  DB_PASSWORD=''
  DB_HOST='127.0.0.1'
  DB_PORT='3306'
    ```
