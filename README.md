Snippit
=======

Code Snippet Application

[![Build Status](https://travis-ci.org/Snippit/snippit.svg?branch=master)](https://travis-ci.org/Snippit/snippit)

[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/Snippit/snippit/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/Snippit/snippit/?branch=master)

Kurulum icin:
git clone git@github.com:Snippit/snippit.git
pip install -r requirements/local.txt

Ornek veri icin
python manage.py loaddata test_accounts test_snippets

Komut ile kullanici olusturmak icin
python manage.py create_user

Tesleri calistirmak icin
python manage.py test account snippet
