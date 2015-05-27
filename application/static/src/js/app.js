//namespace = '/draftboard'; // change to an empty string to use the global namespace
socket = io.connect('http://' + document.domain + ':' + location.port);

var playerControl = require('./playerControl'),
    newPlayer = require('./newPlayer'),
    chatbox = require('./chatbox'),
    playersView = require('./playersView');


chatbox.initialise();
newPlayer.initialise();
playersView.initialise();

$(function() {
    socket.on('connect', function() {
        socket.emit('connect');
    });
});
