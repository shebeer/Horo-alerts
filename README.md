
** How to run test cases
python manage.py test

** How to check code coverage in test
coverage run --source='.' manage.py test 'app_name'
eg: coverage run --source='.' manage.py test core

** How view code coverage report
coverage report