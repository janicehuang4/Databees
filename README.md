#Databees Project 
This is a webstore was done for my CMPSC 431W - Database Management Systems class for the spring 2016 semester. This project was done in a group of five(5).

<b> ** This is a copy of a shared repository in the case the original should be deleted. </b>

## Prerequisites
#### OSX/Linux
* Python 2.7
* Pip (should be installed with python 2.7 installation)
* Virtualenv (pip install virtualenv)
* Virtualenvwrapper (pip install virtualenvwrapper)
* MySQL
* NodeJS (NPM)

#### Windows
##### Be sure to add python2.7 and python2.7/Scripts to you PATH
* Python 2.7
* Pip ( should be installed with the python2.* installation)
* Virtualenv (pip install virtualenv)
* Virtualenvwrapper (pip install virtualenvwrapper-win)
* MySQL
* NodeJS (NPM)

## Launch a project
1. Navigate into databeesProject repo:
   <p>`$ cd databeesProject`
2. Pull latest updates from Github repo:
   <p>`$ git pull`
3. Install gulp and bower dependencies:
   <p>`$ sudo npm install && bower install`
4. Start Gulp:
   <p>`$ gulp`
5. Open new terminal
   <p>
6. Activate virtual environment:
   <p>`$ workon databeesProject`
7. Install package dependencies:
   <p>`$ pip install -r requirements.txt`
8. Navigate into databeesProject directory:
   <p>`$ cd databeesProject`
9. Makemigrations for database:
   <p>`$ ./manage.py makemigrations`
10. Migrate database (update database):
   <p>`$ ./manage.py migrate`
11. Launch the server:
   <p>`$ ./manage.py runserver`

## Localhost Setup
1. Clone the repository:
   <p>`$ git clone https://github.com/yeralin/databeesProject.git databeesProject`

2. Navigate into capstone repo:
   <p>`$ cd databeesProject`

3. Create Virtual Environment Wrapper using Python 2.7:
   <p>`$ mkvirtualenv -p python2.7 databeesProject`

4. Go into you're local environment if not already there:
  	<p>`$ workon databeesProject`
    <p>(databeesProject) should appear at the start of your command prompt

5. Install all the requirements:
	<p>`$ pip install -r requirements.txt`

6. Create local database
    <p>`$ mysql -u root`
    <p>`$ create database databeesproject;`
    <p>`$ quit`

7. Set up the database: (for windows do not include ./)
    <p>`$ ./databeesProject/manage.py migrate`
	  <p>`$ ./databeesProject/manage.py makemigrations`
	  <p>`$ ./databeesProject/manage.py migrate`

8. Install npm packages
    <p>`$ sudo npm install`

9. Install bower and gulp globally
    <p>`$ sudo npm install bower gulp -g`

10. Install bower packages
    <p>`$ bower install`

## MySQL Notes
* When creating the root account, if asked to create a root password, you must
 remove the root password in order to run the syncdb and migrations call.
  <p>`$ mysql -u root -p`
  <p>enter your password
  <p>`SET PASSWORD FOR root@localhost=PASSWORD('');`

* In order to use the mysql -u root, be sure to start your mysql server first. To start or stop the server use these commands
  <p>`$ mysql.server start`
  <p>`$ mysql.server stop`

##Virtual Env Notes
* If you are having issues running the mkvirtualenv or workon commands, make sure you have your vitrual env python and variable are set correctly. Adding these three lines to your .bash_profile should do the trick:
<p> `export WORKON_HOME=$HOME/.virtualenvs`  (This should be set to where ever your .virtualenvs directory is)
<p> `export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3` (This should be set to where ever your Python3 is located)
<p> `source /usr/local/bin/virtualenvwrapper.sh` (This should be where ever your virtualenvwrapper.sh can be found)
* In order to stop working within your virtualenv just type deactivate in your command prompt

## Adding code
Once you have completed your additions to files, run the makefile to check if your
code can be committed. Your code will be checked against the pep8 standards and
a code coverage check will be run. You want to conform to all standards and
have 100% code coverage.

For non-Linux running the make file will be almost impossible to run, you will be able to commit but it is easiest to keep code consistent with these standards in place.


## Migrating
Make sure you add your 'app' to the settings.py under INSTALLED_APPS
You might have to run: 
<p> `./manage.py makemigrations [appName]` 
Before running: 
<p> `./manage.py migrate` 
