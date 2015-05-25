namespace = '/draftboard'; // change to an empty string to use the global namespace
var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);


loseLife = function(id, amount) { socket.emit('lose_life', {'player_id': id, amount: amount}); }

gainLife = function(id, amount) { socket.emit('gain_life', {'player_id': id, amount: amount}); }

createPlayer = function(name) { socket.emit('create_player', {'name': name}); }

socket.on('response', function(data) {
    var $player = $('[data-player-id="' + data.player_id + '"]'),
        life = $player.find('.life-counter');

    life.text(data.life);

    $player.find('.progress-radial').attr('class', 'progress-radial');
    console.log($player);

    var lifePercentage = (parseInt(data.life) * 100) / 20;
    $player.find('.progress-radial').addClass('progress-' + lifePercentage);
});

socket.on('new_player', function(data) {
    var frag = can.view('playerTemplate', data);
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

var playerControl = can.Control.extend({
    init: function(el, opts) {
        console.log('init player control', el, opts);
        this.name = el.find('.player__name').text();
        this._id = el.data('player-id');
    },

    'button.fa-plus click': function(el, ev) {
        console.log('plus life to', this.name);
        gainLife(this._id, 1);
    },

    'button.fa-minus click': function(el, ev) {
        console.log('minus life to', this.name);
        loseLife(this._id, 1);
    }
});

$('.player').each(function() {
    new playerControl(this);
});

new addPlayerForm('form');




