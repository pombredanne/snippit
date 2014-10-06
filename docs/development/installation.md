### Requirements
1. Python 2.7x
2. [PostgreSQL](https://github.com/ivanoats/How-To-Install-PostgreSQL/blob/master/how-to-install-postgres.md) or SQlite
3. [RabbitMQ](https://www.digitalocean.com/community/tutorials/how-to-install-and-manage-rabbitmq)

### Installation

Install Pip and Virtual Environment

    sudo apt-get install python-pip python-dev build-essential
    sudo apt-get install python-pip
    sudo pip install --upgrade pip
    sudo pip install --upgrade virtualenv

Create a virtual env:

    virtualenv snippit
    source snippit/bin/activate

Clone the repository and install requirements:

    cd snippit
    git clone git@github.com:Snippit/snippit.git
    pip install -r snippit/requirements/local.txt

Create local settings file and change default settings
    cp snippit/snippit/settings/local.py.ex snippit/snippit/settings/local.py

To run the project, Follow the following commands:

    cd snippit/
    python manage.py syncdb
    python manage.py migrate
    python manage.py runserver

### To run the tests

    python manage.py test

### Development Hook
[github.com/bahattincinic/python-git-hook](https://github.com/bahattincinic/python-git-hook)

