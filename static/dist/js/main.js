namespace = '/draftboard'; // change to an empty string to use the global namespace
var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);


loseLife = function(id, amount) { socket.emit('lose_life', {'player_id': id, amount: amount}); }

gainLife = function(id, amount) { socket.emit('gain_life', {'player_id': id, amount: amount}); }

createPlayer = function(name) { socket.emit('create_player', {'name': name}); }
broadcastMessage = function(msg) { socket.emit('broadcast_message:send', {'message': msg}); }



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

var chatboxControl = can.Control.extend({
    init: function(el, opts) {
        this.message = el.find('input.message');
        socket.on('broadcast_message:receive', function(data) {
            $('.messages').append('<p class="message">'+data.message+'</p>');
            $('.chatbox').animate({ scrollTop: $('.messages').height() });
        });
    },

    ' submit': function(el, ev) {
        ev.preventDefault();

        if (this.message.val()) {
            broadcastMessage(this.message.val());
            this.message.val('');
        }
    },

    '{toggle} click': function(el, ev) {
        this.options.chatbox.toggleClass('hide');
    }
});

var playerControl = can.Control.extend({
    init: function(el, opts) {
        this.name = el.find('.player__name').text();
        this._id = el.data('player-id');
    },

    'button.fa-plus click': function(el, ev) {
        gainLife(this._id, 1);
    },

    'button.fa-minus click': function(el, ev) {
        loseLife(this._id, 1);
    }
});

$('.player').each(function() {
    new playerControl(this);
});

new addPlayerForm('form.form__player');
new chatboxControl('form.form__chatbox', {
    toggle: $('.chatbox__toggle'),
    chatbox: $('.chatbox')
});




