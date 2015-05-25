# Magic the Gathering Draft scorekeeper

## Setup
```
git clone https://github.com/ackl/draftboard
cd draftboard
pip install virtualenv
virtualenv -p /usr/bin/python2 venv
source venv/bin/activate
pip install -r requirements.txt
cd static
npm install
bower install
gulp
```


## Dev
#### Import some sample players
```
curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/newplayer -d '{"name":"Player 1"}'
curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/newplayer -d '{"name":"Player 2"}'
```


#### Run server
1. Make sure mongodb is running
```
mongod
```
2. Run the Flask app
```
python app.py
```
