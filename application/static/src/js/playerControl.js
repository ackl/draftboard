loseLife = function(id, amount) { socket.emit('lose_life', {'player_id': id, amount: amount}); }

gainLife = function(id, amount) { socket.emit('gain_life', {'player_id': id, amount: amount}); }

var playerControl = can.Control.extend({
    init: function(el, opts) {
        this.name = el.find('.player__name').text();
        this._id = el.data('player-id');
        this.life = parseInt(el.find('.life-counter').text());

        var lifeClassFrag = (this.life * 100) / 20;
        el.find('.progress-radial').addClass('progress-' + lifeClassFrag);
        var that = this;

        socket.on('response', function(data) {
            if (data.player_id == that._id) {
                if (data.life == 0) {
                    that.element.find('button')
                        .addClass('disabled')
                        .attr('disabled', true);
                }
            }
        });
    },

    'button.fa-plus click': function(el, ev) {
        gainLife(this._id, 1);
    },

    'button.fa-minus click': function(el, ev) {
        loseLife(this._id, 1);
    }
});

module.exports = playerControl;
