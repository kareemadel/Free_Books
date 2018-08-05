# Free Books

Introduction
------------
A library application implemented in python3 using the Django framework.

Prerequisites
-------------
* Python>=3.4
* virtualenv

How to Install
----------
```bash
# clone the repo
$ git clone https://github.com/kareemadel/Free_Books
$ cd Free_Books
# create the virtual environemnt
$ mkdir virtualenvironment
$ virtualenv virtualenvironment
$ source virtualenvironment/bin/activate
# first install mysql
$ sudo apt-get install mysql-server libmysqlclient-dev
# create a database 'FreeBooks', add user 'kash' with password 'JHY&*Y(*UYHYG87has', You can change that obviosly but don't to forget to also change it in settings.py
# install the dependencies
$ python3 -m pip install -r Library/requirements.txt
# apply the migrations
$ python3 Library/manage.py migrate
# create admin user
$ python3 Library/manage.py createsuperuser
```

How to Run the App
-----------------------
```bash
$ python3 Library/manage.py runserver
```
