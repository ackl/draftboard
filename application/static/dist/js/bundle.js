(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
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

},{"./chatbox":2,"./newPlayer":3,"./playerControl":4,"./playersView":5}],2:[function(require,module,exports){
broadcastMessage = function(msg) { socket.emit('broadcast_message:send', {'message': msg}); }

var chatboxControl = can.Control.extend({
    init: function(el, opts) {
        this.message = el.find('input.message-area');
        socket.on('broadcast_message:receive', function(data) {
            alert(data.message);
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

module.exports = {
    initialise: function() {
        new chatboxControl('form.form__chatbox', {
            toggle: $('.chatbox__toggle'),
            chatbox: $('.chatbox')
        });
    }
}

},{}],3:[function(require,module,exports){
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





},{"./playerControl":4}],4:[function(require,module,exports){
loseLife = function(id, amount) { socket.emit('lose_life', {'player_id': id, amount: amount}); }

gainLife = function(id, amount) { socket.emit('gain_life', {'player_id': id, amount: amount}); }

var playerControl = can.Control.extend({
    init: function(el, opts) {
        this.name = el.find('.player__name').text();
        this._id = el.data('player-id');
        this.life = parseInt(el.find('.life-counter').text());

        var lifeClassFrag = (this.life * 100) / 20;
        el.find('.progress-radial').addClass('progress-' + lifeClassFrag);
    },

    'button.fa-plus click': function(el, ev) {
        gainLife(this._id, 1);
    },

    'button.fa-minus click': function(el, ev) {
        loseLife(this._id, 1);
    }
});

module.exports = playerControl;

},{}],5:[function(require,module,exports){
var playerControl = require('./playerControl');

Player = can.Model.extend({
    get: function() {
        return $.get('/api/players')
    }
}, {});


module.exports = {
    initialise: function() {
        new Player.get().then(function(data) {
            can.each(data, function(item) {
                item._id = item._id.$oid;
                console.log(item);
                //item.attr('_id', item.attr('_id.$oid'));
                //console.log(item.attr('_id'))
                var frag = can.view('playerTemplate', {'player': item}, {
                    testingFunc: function() {
                        return 'hi'
                    }
                });
                $('.players.row').append(frag);
                new playerControl($('.players.row').find('.player').last());
            });
        });
    }
}


},{"./playerControl":4}]},{},[1]);

//# sourceMappingURL=bundle.js.map