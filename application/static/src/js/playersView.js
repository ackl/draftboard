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
                item._id = item._id || item.id;
                item._id = item._id.$oid;
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

