$(document).ready(function() {
    let csrftoken = $('[name=csrfmiddlewaretoken]').val();
$('.funcBtn').on('click', function() {
    element = $(this);
    console.log(element)
    id = element.attr('id');
    let xhttp = new XMLHttpRequest();
    xhttp.responseType = 'json';
    let url = location.protocol + '//' + location.host + location.pathname+ $(this).closest('.aauthor').attr('id');
    xhttp.open('POST', url.replace('authors', 'author'));
    xhttp.setRequestHeader('X-CSRFToken', csrftoken);
    if (id === 'follow') {
        element.addClass('active_btn');
        element.removeClass('inactive_btn');
        element.text('Unfollow');
        element.attr('id', 'unfollow');
        xhttp.send('{"follow": "t", "unfollow": ""}');
    } else if (id === 'unfollow') {
        element.removeClass('active_btn');
        element.addClass('inactive_btn');
        element.text('+ Follow');
        element.attr('id', 'follow');
        xhttp.send('{"follow": "", "unfollow": "t"}');
    }
    });
    });
