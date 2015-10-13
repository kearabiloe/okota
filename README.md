# okota

Okota is the official CMS of the now closed okota.co.za - Made public only for educational and testing purposes.

`requirements.txt` file is:

```
Django==1.7
Pillow==2.3.0
virtualenv==1.11.4
psycopg2==2.5.3
```

## Installation
The default installation directory for okota is /var/www/okota.co.za/. It is advisable that you replicate the same configurations on your machine, otherwise make the neccessary changes in settings.py and wsgi.py.

### 1. Directory
'$ cd /var/www/'

'$ mkdir okota.co.za && cd okota.co.za'

### 2. virtualenv / virtualenvwrapper

`$ mkvirtualenv --clear env`

### 3. Download
Now, you need the *django-sample-app* project files in your workspace:

    $ git clone git@github.com:kearabiloe/okota.git okota && cd okota

### 4. Requirements
Install the *requirements.txt* file:

`$ pip install -r requirements.txt`


#### local.py (development specific) settings file
Copy `configs/settings.py` & `configs/wsgi.py`  into the 'okota_website' folder.
Remember to change server specific settings including the database credentials

#### Sample Databse (Testing specific) dump  file
Restore the 'sample.dump' file using pg_restore

#### Initialize the database

`./manage.py makemigrations okota`

`./manage.py migrate okota `

### Ready? Go!

`./manage.py runserver`

Navigate to 127.0.0.1:8000/ on your browser!!!