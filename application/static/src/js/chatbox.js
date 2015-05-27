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
