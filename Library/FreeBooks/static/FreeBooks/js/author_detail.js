function swapElements(e, t, i) {
    e.show(), t.hide(), 'more' == $(i).text() ? $(i).text('(less)') : $(i).text('more');
}

function swapContent(e) {
    let t = $(e).data('id');
    i = $(e).siblings('#freeTextContainer' + t);
    o = $(e).siblings('#freeText' + t);
    'none' == i.css('display') ? swapElements(i, o, e) : 'none' == o.css('display') && swapElements(o, i, e);
}