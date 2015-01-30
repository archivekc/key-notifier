set PREVIOUSPY=%PYTHONPATH%
set PYTHONPATH=.;../PIL;%PYTHONPATH%

cd src
python launcher.py
cd ..

set PYTHONPATH=%PREVIOUSPY%
