$(document).ready(function () {
    let chatContainer=$(".chat-container");
    let input=$(".msg");
    let send=$("#send");
    reciver=$("#reciver_id");

    send.click(function(){
        message=input.val();
        $.ajax({
            type: "POST",
            url: "/send_msg",
            data: {message:message,reciver:reciver.val()},
            success: function (response) {
                console.log(response);
            }
        });
    })


    $.ajax({
        type: "POST",
        url: "/get_send_msg",
        data: {reciver:reciver.val()},
        success: function (response) {
            let rightPart=$('<div>').addClass('right-part');
            let msgRight=$('<div>').addClass('msg-right');
            $.each(response, function (index, value) { 
                let span=$("<span>").html(value.send_msg);
                msgRight.append(span);
                rightPart.append(msgRight);
            });
            chatContainer.prepend(rightPart);
        }
    });
    $.ajax({
        type: "POST",
        url: "/get_recived_msg",
        data: {reciver:reciver.val()},
        success: function (response) {
            let leftPart=$('<div class="left-part">').addClass('left-part');
            let msgLeft=$('<div>').addClass('msg-left');
            $.each(response, function (index, value) { 
                let span=$("<span>").html(value.recived_msg);
                msgLeft.append(span);
                leftPart.append(msgLeft);
            });
            chatContainer.prepend(leftPart);
        }
    });

})