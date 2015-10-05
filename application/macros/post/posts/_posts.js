// 收藏文章
$(document).on('click', '.m-post .btn-collect-post', function () {
    var postId = $(this).data('post-id'),
        collected = $(this).hasClass('collected'),
        url = "",
        _this = $(this);

    if (collected) {
        url = urlFor('blog.uncollect_post', {uid: postId});
    } else {
        url = urlFor('blog.collect_post', {uid: postId});
    }

    $.ajax({
        url: url,
        method: 'post',
        dataType: 'json'
    }).done(function (response) {
        if (response.result) {
            if (collected) {
                _this.removeClass('collected');
            } else {
                _this.addClass('collected');
            }
        }
    });
});
