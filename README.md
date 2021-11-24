### Server installation Instructions

- clone the project
- cd D-Nothi
- create virtual environment and active virtual environment
  - $ virtualenv venv
  - $ source venv/bin/activate
- Install project dependencies
  -  pip install -r requirements.txt
- Run migration
    - python manage.py migrate
- collect static files
  - python manage.py collectstatic
- Start development server
   - python manager.py runserver


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
