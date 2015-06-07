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
                var frag = can.view('playerTemplate', {'player': item}, {
                    getScore: function(match, player_id) {
                        return match.player_scores[player_id].toString();
                    }
                });

                $('.players.row').append(frag);
                new playerControl($('.players.row').find('.player').last());
            });
        });

    }
}

