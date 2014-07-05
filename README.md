Snippit.in
=======

Code Snippet Application

[![Build Status](https://travis-ci.org/Snippit/snippit.svg?branch=master)](https://travis-ci.org/Snippit/snippit) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/Snippit/snippit/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/Snippit/snippit/?branch=master) [![Requirements Status](https://requires.io/github/Snippit/snippit/requirements.png?branch=master)](https://requires.io/github/Snippit/snippit/requirements/?branch=master)


=======
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

To run the project, Follow the following commands:

    cd snippit/
    python manage.py syncdb
    python manage.py runserver

### To run the tests

    python manage.py test account.tests snippet.tests auth.tests

### Development Hook
[github.com/cbrueffer/pep8-git-hook](https://github.com/cbrueffer/pep8-git-hook)


## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request
