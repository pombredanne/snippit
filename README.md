Snippit.in
=======

Code Snippet Application

[![Build Status](https://travis-ci.org/Snippit/snippit.svg?branch=master)](https://travis-ci.org/Snippit/snippit) [![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/Snippit/snippit/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/Snippit/snippit/?branch=master)

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/Snippit/snippit/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/Snippit/snippit/?branch=master)

=======
### Installation

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
