### Server installation Instructions

- **clone the project**
  ```bash
   $ git clone git@github.com:shahid-ullah/D-Nothi.git
   ```
- **change to project directory**
  ```bash
  $ cd D-Nothi
  ```
- **create virtual environment and active virtual environment**
  ```bash
    $ virtualenv venv
    $ source venv/bin/activate
  ```
- **Install project dependencies**
  ```bash
    $ pip install -r requirements.txt
  ```
- **Run migration**
  ```bash
    $ python manage.py migrate automate_process --database='source_db'
    $ python manage.py migrate backup_source_db --database='backup_source_db'
    $ python manage.py migrate dashboard_generate --database='default'
    $ python manage.py migrate users --database='default'
  ```
- **collect static files**
  ```bash
    $ python manage.py collectstatic
  ```
- **Start development server**
  ```bash
    $ python manager.py runserver
  ```

### Additional Instructions

- create .env file in project root directory and put required value

```py
  SECRET_KEY=''
  DEBUG=False
  DB_NAME=''
  DB_USER=''
  DB_PASSWORD=''
  DB_HOST=''
  DB_PORT=''
  SOURCE_DB_NAME=''
  SOURCE_DB_USER=''
  SOURCE_DB_PASSWORD=''
  SOURCE_DB_HOST=''
  SOURCE_DB_PORT=''
  BACKUP_SOURCE_DB_NAME=''
  BACKUP_SOURCE_DB_USER=''
  BACKUP_SOURCE_DB_PASSWORD=''
  BACKUP_SOURCE_DB_HOST=''
  BACKUP_SOURCE_DB_PORT=''
```
