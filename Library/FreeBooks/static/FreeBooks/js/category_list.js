$(document).ready(function() {
    let csrftoken = $('[name=csrfmiddlewaretoken]').val();
$('.funcBtn').on('click', function() {
    element = $(this);
    id = element.attr('id');
    let xhttp = new XMLHttpRequest();
    xhttp.responseType = 'json';
    let url = location.protocol + '//' + location.host + location.pathname+ $(this).closest('.acategory').attr('id');
    xhttp.open('POST', url.replace(/(?:Favourite|categories)/, 'categoriesBooks'));
    xhttp.setRequestHeader('X-CSRFToken', csrftoken);
    console.log(id);
    if (id === 'favourite') {
        element.addClass('active_btn');
        element.removeClass('inactive_btn');
        element.text('❤');
        element.attr('id', 'unfavourite');
        xhttp.send('{"favourite": "t", "unfavourite": ""}');
    } else if (id === 'unfavourite') {
        element.removeClass('active_btn');
        element.addClass('inactive_btn');
        element.text('favourite');
        element.attr('id', 'favourite');
        xhttp.send('{"favourite": "", "unfavourite": "t"}');
    }
    });
    });
