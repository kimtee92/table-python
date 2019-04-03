#!flask/bin/python
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/all": {"origins": "*"}})
socketio = SocketIO(app)
 
app.config['MONGO_DBNAME'] = 'guestbook'
app.config['MONGO_URI'] = 'mongodb+srv://dbguest:NSN9mGkU0jfQUFDs@cluster0-at0kr.mongodb.net/guestbook?retryWrites=true'
mongo = PyMongo(app)

@app.route('/all', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type','Authorization', 'Access-Control-Allow-Origin'])
def all():
  guests = mongo.db.guests
  output = []
  for g in guests.find():
    output.append({'Name' : g['Name'], 'Email' : g['Email'], 'Address' : g['Address'], 'Date' : g['Date']})
  return jsonify(output)

"""
@app.route('/star', methods=['POST'])
def add_star():
  star = mongo.db.stars
  name = request.json['name']
  distance = request.json['distance']
  star_id = star.insert({'name': name, 'distance': distance})
  new_star = star.find_one({'_id': star_id })
  output = {'name' : new_star['name'], 'distance' : new_star['distance']}
  return jsonify({'result' : output})
"""

@socketio.on('connect')
def test_connect():
    print('connect', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@socketio.on('guest')
def handle_guest(guest):
    print('received guest: ' + str(guest))
    emit('guest', guest, broadcast=True)
    guests = mongo.db.guests
    guests.insert(guest)
    print(guest)
    


if __name__ == '__main__':
    socketio.run(app)
