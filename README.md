# Aimo notes

API created to manage notes

## Setup
```
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```
## Banck-end server
To start it run
```
python3 server/manage.py start-server
```
Runs by default at http://localhost:8000


Other execution parameters can be passed. To see the help run:
```
python3 server/manage.py start-server -h
```
It will show:
```
Usage: manage.py start-server [OPTIONS]

Options:

-ip, --ip TEXT Set application server ip

-p, --port INTEGER Set application server port

-d, --debug INTEGER Set application server debug. 0 -> False. 1 -> True

-h, --help Show this message and exit.
```
The parameters can also be set in an .env file that is lifted from the root of the project. Check [.env.sample](https://github.com/EduuardoPerez/Aimo-notes/blob/master/.env.sample) file for watch the possible variables.

### Available end-points
| End-point|HTTP Methods|
| ------- | ----- |
| /users/signup/ | POST |
| /notes/ | GET & POST |