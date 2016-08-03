var csrftoken = $.cookie('csrftoken');
var last_received = 0;

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$(document).ready(function() {
    $('#chat_form').submit(function(){
        var $inputs = $(this).children('input');
        var values = {};
        $inputs.each(function(i,el) {
            values[el.name] = $(el).val();
        });
        $.ajax({
            type: 'post',
            url: '/post/',
            data: values,
            dataType: 'json'

        });
        $('#messageText').val('');
        return false;
    });
    sync_messages();
});

function sync_messages() {
    $.ajax({
        type: 'post',
        url:'/sync/',
		dataType: 'json',
        content_type: 'application/json',
		success: function (json) {
            last_received = json.lmid;
		},
        error: function(jqXHR, textStatus, errorThrown) {
            console.log(errorThrown);
        }
    });

	setTimeout("get_messages()", 2000);
}

function get_messages() {
    $.ajax({
        type: 'post',
        url:'/receive/',
        data: {offset: window.last_received},
		dataType: 'json',
		success: function (json) {
			// add messages
            //alert(json.result);
			$.each(json.result, function(i,m){
                $('.media-list').append('<li>' + m.message + '<span class="text-success"> -' + m.sender + '</span></li>');
                last_received = m.id;
			});
			$("#media-list").animate({ scrollTop: $(this) }, 500);
		},
        error: function(jqXHR, textStatus, errorThrown){
            console.log(errorThrown);
        }
    });

    // wait for next
    setTimeout("get_messages()", 2000);
}