Flasky
======

This repository contains the source code examples for the book [Flask Web Development](http://www.flaskbook.com).

The commits and tags in this repository were carefully created to match the sequence in which concepts are presented in the book. Please read the section titled "How to Work with the Example Code" in the book's preface for instructions.

This repo is revised by [Harry Wang](https://github.com/harrywang) for teaching Web Application Development

## Setup Instructions:

Make sure to use Python version 2.7.x.

Install `virtualenv` if needed.

If you do not have a virtual environment yet on the project folder, set it up with:

    $ virtualenv venv

Then activate the virtual environment

    $ source venv/bin/activate

Install packages (use dev.txt during development)

    $ pip install -r requirements/dev.txt

Deploy: this create the tables in the database and populate the init data

    $ python manage.py deploy

Run the server

    $ python manage.py runserver

Run the tests

    $ python manager.py test

Then go to browser and type in the address bar

    127.0.0.1:5000

To use the shell during development:

    $ python manage.py shell
