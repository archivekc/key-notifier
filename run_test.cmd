set PREVIOUSPY=%PYTHONPATH%
set PYTHONPATH=src;%PYTHONPATH%

python -m unittest test/TimeFilterTest.py test/TANTest.py test/biclooTest.py test/jenkinsTest.py test/RSSTest.py

set PYTHONPATH=%PREVIOUSPY%
