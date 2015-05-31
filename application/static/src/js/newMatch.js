var playerControl = require('./playerControl');

var newMatchControl = can.Control.extend({
    init: function(el, opts) {
        //this.element.find('input:checked') = el.find('input:checked');
        if (!el.find('input').length) {
            el.html('<p>No players are available for a game right now</p>');
        }

        this.$bestOf = el.find(opts.bestOf);
    },

    'button.start-game click': function(el, ev) {
        var playerScores = {};

        this.element.find('input:checked').each(function() {
            var playerId = $(this).attr('id');
            playerScores[playerId] = 0;
        });


        console.log(JSON.stringify({'player_scores': playerScores}));
        var bestOf = this.$bestOf[this.$bestOf.filter('.selected').index()].innerText;
        console.log(bestOf);

        $.ajax({
            type: 'POST',
            url: '/api/matches/',
            data: JSON.stringify({
                player_scores: JSON.stringify(playerScores),
                best_of: bestOf
            }),
            contentType: 'application/json; charset=utf-8',
            dataType: 'json'
        }).then(function(data) {
            console.log(data);
            if ('is_ongoing' in data) {
                location.href = '/matches/' + data._id;
            }
        });
    },

    'input:checkbox change': function(el, ev) {
        var button = this.element.find('button')
        if (this.element.find('input:checked').length > 1 && !this.valid) {
            button.removeClass('disabled').attr('disabled', false);
        } else {
            button.addClass('disabled').attr('disabled', true);
        }
    },

    '{bestOf} click': function(el, ev) {
        this.$bestOf.removeClass('selected');
        el.addClass('selected');
    }
});


module.exports = {
    initialise: function() {
        new Player.get().then(function(data) {

            var freePlayers = data.filter(function(item) {
                return !('current_match' in item)
            });


            var frag = can.view('freePlayersListTemplate', {'players': freePlayers}, {});
            $('.page').append(frag);

            new newMatchControl('.free-players', {bestOf: '.best-of__option'});
        });
    }
}

