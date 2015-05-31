Match = can.Model.extend({
    get: function() {
        return $.get('/api/matches')
    }
}, {});


module.exports = {
    initialise: function() {
        new Match.get().then(function(data) {
            console.log(data)
            var frag = can.view('MatchListTemplate', {'games': data}, {});
            $('.page').append(frag);
        });
    }
}

