Match = can.Model.extend({
    get: function() {
        return $.get('/api/matches')
    }
}, {});


module.exports = {
    initialise: function() {
        new Match.get().then(function(data) {
            console.log(data)
            var frag = can.view('playersListTemplate', {'games': data}, {
                renderPlayers: function(a, b) {
                    console.log('renderplayers', a, b);
                    console.log(Object.keys(a));
                    return Object.keys(a);

                }
            });
            $('.page').append(frag);
        });
    }
}

