$(document).ready(function() {
    let csrftoken = $('[name=csrfmiddlewaretoken]').val();
    /* 1. Visualizing things on Hover - See next part for action on click */
    $('#stars li').on('mouseover', function() {
        // The star currently mouse on
        let onStar = parseInt($(this).data('value'), 10);
        // Now highlight all the stars that's not after the current hovered star
        $(this).parent().children('li.star').each(function(e) {
            if (e < onStar) {
                $(this).addClass('hover');
            } else {
                $(this).removeClass('hover');
            }
        });
    }).on('mouseout', function() {
        $(this).parent().children('li.star').each(function(e) {
            $(this).removeClass('hover');
        });
    });

    /* 2. Action to perform on click */
    $('#stars li').on('click', function() {
        // The star currently selected
        let onStar = parseInt($(this).data('value'), 10);
        let stars = $(this).parent().children('li.star');

        for (i = 0; i < stars.length; i++) {
            $(stars[i]).removeClass('selected');
        }

        for (i = 0; i < onStar; i++) {
            $(stars[i]).addClass('selected');
        }

        // JUST RESPONSE (Not needed)
        let ratingValue = parseInt($(this).data('value'));
        console.log(ratingValue);
        let xhttp = new XMLHttpRequest();
        xhttp.responseType = 'json';
        let url = location.protocol + '//' + location.host + location.pathname + $(this).closest('.abook').attr('id');
        xhttp.open('POST', url.replace('books', 'book'));
        xhttp.setRequestHeader('X-CSRFToken', csrftoken);
        xhttp.send('{"rate": ' + ratingValue + '}');
    });

    $('.funcBtn').on('click', function() {
        element = $(this);
        id = element.attr('id');
        let xhttp = new XMLHttpRequest();
        xhttp.responseType = 'json';
        let url = location.protocol + '//' + location.host + location.pathname + $(this).closest('.abook').attr('id');
        xhttp.open('POST', url.replace('books', 'book'));
        xhttp.setRequestHeader('X-CSRFToken', csrftoken);
        if (id === 'read') {
            element.addClass('active_btn');
            element.removeClass('inactive_btn');
            element.text('Done ✔');
            element.attr('id', 'unread');
            wish = $(this).siblings('#unwish');
            wish.removeClass('active_btn');
            wish.addClass('inactive_btn');
            wish.text('Wish to Read');
            wish.attr('id', 'wish');
            $(this).siblings('#wish, #unwish').css({'display': 'none'});
            xhttp.send('{"read": "t", "unread": "", "wish": "", "unwish": "t"}');
        } else if (id === 'unread') {
            element.removeClass('active_btn');
            element.addClass('inactive_btn');
            element.text('Read');
            element.attr('id', 'read');
            $(this).siblings('#wish, #unwish').css({'display': ''});
            xhttp.send('{"read": "", "unread": "t"}');
        } else if (id === 'wish') {
            element.addClass('active_btn');
            element.removeClass('inactive_btn');
            element.text('Will Read! ✔');
            element.attr('id', 'unwish');
            read = $(this).siblings('#unread');
            read.removeClass('active_btn');
            read.addClass('inactive_btn');
            read.text('Read');
            read.attr('id', 'read');
            xhttp.send('{"read": "", "unread": "", "wish": "t", "unwish": ""}');
        } else if (id === 'unwish') {
            element.removeClass('active_btn');
            element.addClass('inactive_btn');
            element.text('Wish to Read');
            element.attr('id', 'wish');
            xhttp.send('{"wish": "", "unwish": "t"}');
        }
    });
});
