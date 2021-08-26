Basketball Tournament Management System
---------------------------------------

Python version used: 3.8.10

Import Data
python3 manage.py load_pet_data
SQLLite DB: db.sqlite3 

Start application
python3 manage.py runserver

Available Services

Home page: http://localhost:8000/

List all games: GET http://localhost:8000/games/
sample: curl -X GET 'http://localhost:8000/games/' -v

Champion Team: GET http://localhost:8000/winnerteam/
sample: curl -X GET 'http://localhost:8000/winnerteam/' -v
