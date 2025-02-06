# QuizGPT Backend Setup (end user-facing)

## Set environmental variables

### Set the PostgreSQL database url:

``DATABASE_URL=postgresql://postgres:postgres@localhost:5432/quiz-app``

## Set up the Python venv

### Run:

``python3 -m venv env``\
``source env/bin/activate``

## Install dependencies

### Run:

``pip install -r requirements.txt``

## Start the server

### Run:

``flask --app app run``
