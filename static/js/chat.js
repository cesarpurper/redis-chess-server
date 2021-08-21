
var Message;
Message = function (arg) {
    this.text = arg.text, 
    this.message_side = arg.message_side,
    this.avatar = arg.avatar;
    this.draw = function (_this) {
        return function () {
            var $message;
            $message = $($('.message_template').clone().html());
            $message.addClass(_this.message_side).find('.text').html(_this.text);
            $message.find('.avatarP').attr("data-letters",_this.avatar);
            $('.messages').append($message);
            return setTimeout(function () {
                return $message.addClass('appeared');
            }, 0);
        };
    }(this);
    return this;
};

drawMessages = function (messages, nick) {
    $.each(messages, function (index, value) {
        var side;
        if (value.nick == nick)
            side = 'right'
        else {
            side = 'left'
        }
        message = new Message({
            text: value.message,
            message_side: side,
            avatar : nick.toUpperCase().substring(0, 1)
        })
        message.draw();
    });
}

sendMessage = function(text, nick, roomName){
    data = {
        message : text,
        nick: nick,
        time: Date.now()
    }
    $.ajax({
        type: "POST",
        url: "http://localhost:5000/message",
        data: {
            data : JSON.stringify(data),
            roomName : roomName

        }
      });
      $(".message_input").val("")
}

writeMessage = function (data,nick) {
    var side;
    $messages = $(".messages")
    if (data.nick == nick)
        side = 'right'
    else {
        side = 'left'
    }
    message = new Message({
        text: data.message,
        message_side: side,
        avatar : data.nick.toUpperCase().substring(0, 1)
    })
    message.draw();
    return $messages.animate({ scrollTop: $messages.prop('scrollHeight') }, 300);

};


