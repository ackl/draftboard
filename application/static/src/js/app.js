//namespace = '/draftboard'; // change to an empty string to use the global namespace
socket = io.connect('http://' + document.domain + ':' + location.port);

var playerControl = require('./playerControl'),
    newPlayer = require('./newPlayer'),
    chatbox = require('./chatbox'),
    playersView = require('./playersView'),
    gamesView = require('./gamesView'),
    newMatch = require('./newMatch');


chatbox.initialise();


$(function() {
    socket.on('connect', function() {
        socket.emit('connect');
    });




    var path = location.pathname;

    if (path === '/') {
        newPlayer.initialise();
        playersView.initialise();

    } else if (path === '/matches') {
        gamesView.initialise();

    } else if (path.split('/').length === 3 && path.split('/')[1] === 'matches') {

        if (path.split('/')[2] === 'new') {
            console.log('init new match');
            newMatch.initialise();

        } else {
            console.log('init match')
            $('[data-player-id]').each(function() {
                new playerControl(this);
            });
        }
    }
});
