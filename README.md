# School Pocket
A very simple web app to manage a student's career written in Python using Flask framework

Recap
------------------
This project began as a high school graduation project written entirely in PHP.
Subsequently it was rewritten in Ruby and Python (using RoR and Flask), to improve my webdev skills.


Installation
--------
Clone the repo:

`$ git clone https://github.com/andreacrispo/school-pocket-py.git`
`$ cd school-pocket-py/`

Create virtual environment
`$ virtualenv venv`
`$ source venv/bin/activate`

Install dependencies

`$ pip install -r requirements.txt`

Migrate database 

`$ python manage.py db migrate`

Launch built-in web server

`$ python manage.py runserver`
