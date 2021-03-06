function swapElements(e, t, i) {
    e.show(), t.hide(), 'more' == $(i).text() ? $(i).text('(less)') : $(i).text('more');
}

function swapContent(e) {
    let t = $(e).data('id');
    i = $(e).siblings('#freeTextContainer' + t);
    o = $(e).siblings('#freeText' + t);
    'none' == i.css('display') ? swapElements(i, o, e) : 'none' == o.css('display') && swapElements(o, i, e);
}
$(document).ready(function() {
    let csrftoken = $('[name=csrfmiddlewaretoken]').val();
$('.funcBtn').on('click', function() {
    element = $(this);
    id = element.attr('id');
    let xhttp = new XMLHttpRequest();
    xhttp.responseType = 'json';
    let url = location.protocol + '//' + location.host + location.pathname;
    xhttp.open('POST',url);
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
