from flask import Flask, request, render_template
from flask_cors import CORS
from random import randint
import redis
import json
import os

#initializing the redis server connection
redis = redis.Redis(host="redis", port=6379)

#when initializing the server 
redis.flushall()

#initializing the flask application 
app = Flask("teste", static_url_path='')
CORS(app, resources={r"/*": {"origins": "*"}})

#this variable keeps count of the amount of rooms created
#if it doesn't exists redis create it with value '1'
nroSala = redis.incr("roomCount", 1) 
playerCount = 0 

#this function pushes a value to a list 'roomName:game'. This value is a FEN chess notation so each play is kept in this list, recording the path the board pieces have made.
@app.route('/play',methods=['POST'])
def play():
	message = request.form.get("data")
	roomName = request.form.get("roomName")
	redis.lpush(roomName+":game", message)
	return ''

#this function pushes a value to a list 'roomName:chat'. This value is chat message sent by any player so this list keeps the whole conversation between players
@app.route('/message',methods=['POST'])
def message():
	message = request.form.get("data")
	roomName = request.form.get("roomName")
	redis.lpush(roomName+":chat", message)
	return ''

#this function concatenate the information recorded in both 'roomName:chat' and 'roomName:game' variables, and return it in a JSON format
@app.route('/getRoomData',methods=['GET'])
def getRoomData():
	roomName = request.args.get('roomName')
	roomData = {
		"game": [],
		"chat":[]
	}
	gameListRedis = redis.lrange(roomName+":game", 0, -1 )
	if gameListRedis != None:
		for x in gameListRedis:
			roomData["game"].append(json.dumps(str(x.decode('utf-8'))))
	chatListRedis = redis.lrange(roomName+":chat", 0, -1 )
	if chatListRedis != None:
		for x in chatListRedis:
			roomData["chat"].append(json.dumps(str(x.decode('utf-8'))))
	
	return json.dumps(roomData)

#this function handles the 'matchmaking'. It just matches people as they are logging in. If the player logs, and there is no one waiting to play, 
#he will have to wait till someone ente rto play, and this function will handle this. 
@app.route('/joinRoom',methods=['GET'])
def joinRoom():
	#get nick from query arguments
	nick = request.args.get('nick')	
	player = 1
	global nroSala, playerCount
	
	if playerCount % 2 == 0:
		#increments global room count
		nroSala = redis.incr("roomCount", 1)
	else:
		player = 2
	
	playerCount += 1

	roomName = "room:"+str(nroSala)	

	#increment room players count
	redis.incr(roomName+":nr", 1)

	#push into list player logged
	redis.lpush(roomName+":players", nick) 
	
	return '{"roomName": "'+roomName+'", "playerNmbr": '+str(player)+'}'

#this function will be called in loop by the player logged that is waiting a opponent. 
@app.route('/getPlayers',methods=['GET'])
def getPlayers():
	roomName = request.args.get('roomName')
	players = []

	#search for players list, iterate, decodes and put it into a players python array
	for x in redis.lrange(roomName+":players", 0, -1 ):
		players.append(str(x.decode('utf-8')))
	
	return json.dumps(players)

#the main function called to render the frontend page
@app.route('/',methods=['GET'])
def root():
	return render_template("game2.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

