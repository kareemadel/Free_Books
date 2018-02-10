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
        let ratingValue = parseInt($('#stars li.selected').last().data('value'), 10);
        let msg = '';
        if (ratingValue > 1) {
            msg = 'Thanks! You rated this ' + ratingValue + ' stars.';
        } else {
            msg = 'We will improve ourselves. You rated this ' + ratingValue + ' stars.';
        }
        responseMessage(msg);
    });
});
