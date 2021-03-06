### Server installation Instructions

- **clone the project**
  - `$ git clone git@github.com:shahid-ullah/D-Nothi.git`
- **change to project directory**
  - `$ cd D-Nothi`
- **create virtual environment and active virtual environment**
  - `$ virtualenv venv`
  - `$ source venv/bin/activate`
- **Install project dependencies**
  - `$ pip install -r requirements.txt`
- **Run migration**
  - `$ python manage.py migrate`
- **collect static files**
  - `$ python manage.py collectstatic`
- **Start development server**
  - `$ python manager.py runserver`

### Additional Instructions

- create .env file in project root directory and put required value

```
  SECRET_KEY=''
  DEBUG=False
  DB_NAME=''
  DB_USER=''
  DB_PASSWORD=''
  DB_HOST='127.0.0.1'
  DB_PORT='3306'
  SOURCE_DB_NAME=''
  SOURCE_DB_USER=''
  SOURCE_DB_PASSWORD=''
  SOURCE_DB_HOST=''
  SOURCE_DB_PORT=''
```
