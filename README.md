# redis-chess-server
_This is a easy to set-up and play chess web server using redis_

## Objectives

This chess server was made to practice the usage of redis in a use case application. 


## Installation

To download and setup the server, just follow these easy steps

```sh
git clone https://github.com/cesarpurper/redis-chess-server.git
cd redis-chess-server
docker-compose up
```

## How to play

By default the server listens to the 5000 port, so the server is accessible in the http://localhost:5000 url.

The matchmaking system is pretty simple, it pairs people as they log into the server.

To log in in the matchmaking queue, just the nickname is needed in the home page the server will show, as the following image shows.


[IMAGE LOG IN]


After that, the logged player will have to wait till an opponent log in so the match can start. No ranking system is in play for this as mentioned earlier.

When the opponent logs in and the players are matched, tha game starts. The game UI is composed by the chess board and a chat room, that players can communicate with each other.

[IMAGE IN PLAY]





