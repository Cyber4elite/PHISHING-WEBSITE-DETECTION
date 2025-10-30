@echo off
echo Setting up PhishShield Virtual Environment
echo ==========================================

echo.
echo 1. Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo 2. Checking Python version...
python --version

echo.
echo 3. Installing dependencies...
pip install -r requirements\development.txt

echo.
echo 4. Running database migrations...
python manage.py migrate

echo.
echo 5. Collecting static files...
python manage.py collectstatic --noinput

echo.
echo 6. Running system checks...
python manage.py check

echo.
echo 7. Testing the application...
python main.py --check

echo.
echo ==========================================
echo Virtual environment setup complete!
echo.
echo To start the application:
echo 1. Run: setup_venv.bat
echo 2. Then run: python main.py
echo.
pause
