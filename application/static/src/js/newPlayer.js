var playerControl = require('./playerControl');

//createPlayer = function(name) { socket.emit('create_player', {'name': name}); }
//
createPlayer = function(name) {
    $.ajax({
        type: 'POST',
        url: '/api/players/',
        data: JSON.stringify({name: name}),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json'
    });
}


    socket.on('devtest', function(data) {
        console.log(data);
    });


socket.on('response', function(data) {
    var $player = $('[data-player-id="' + data.player_id + '"]'),
        life = $player.find('.life-counter');

    life.text(data.life);

    $player.find('.progress-radial').attr('class', 'progress-radial');

    var lifePercentage = (parseInt(data.life) * 100) / 20;
    lifePercentage = (lifePercentage < 1) ? 0 : lifePercentage;
    $player.find('.progress-radial').addClass('progress-' + lifePercentage);
});

socket.on('new_player', function(data) {
    console.log(data)
    var frag = can.view('playerTemplate', data, {
        testingFunc: function() {
            return 'hi'
        }
    });
    $('.players.row').append(frag);
    new playerControl($('.players.row').find('.player').last());
});

var addPlayerForm = can.Control.extend({
    init: function(el, opts) {
        this.name = el.find('input.name')
    },

    ' submit': function(el, ev) {
        ev.preventDefault();

        if (this.name.val()) {
            createPlayer(this.name.val());
            this.name.val('');
        }
    }
});


module.exports = {
    initialise: function() {
        new addPlayerForm('form.form__player');
    }
}




