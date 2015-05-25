# Magic the Gathering Draft scorekeeper

## Setup
```
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```


## Dev
#### Import some sample players
```
curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/newplayer -d '{"name":"Player 1"}'
curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/newplayer -d '{"name":"Player 2"}'
```


#### Run server
python app.py
