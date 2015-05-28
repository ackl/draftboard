//namespace = '/draftboard'; // change to an empty string to use the global namespace
socket = io.connect('http://' + document.domain + ':' + location.port);

var playerControl = require('./playerControl'),
    newPlayer = require('./newPlayer'),
    chatbox = require('./chatbox'),
    playersView = require('./playersView'),
    gamesView = require('./gamesView');


chatbox.initialise();

var path = location.pathname;

if (path === '/') {
    newPlayer.initialise();
    playersView.initialise();
} else if (path === '/matches') {
    gamesView.initialise();
}

$(function() {
    socket.on('connect', function() {
        socket.emit('connect');
    });
});
