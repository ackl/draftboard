namespace = '/draftboard'; // change to an empty string to use the global namespace
socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

var playerControl = require('./playerControl');
var newPlayer = require('./newPlayer');
var chatbox = require('./chatbox');

$('.player').each(function() {
    new playerControl(this);
});

chatbox.initialise();
newPlayer.initialise();
