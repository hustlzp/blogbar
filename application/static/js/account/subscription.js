// 将所有文章标记为已读
$('.btn-mark-all-posts').click(function () {
    $.ajax({
        url: '/account/mark_all_posts',
        dataType: 'json',
        method: 'post'
    }).done(function (response) {
        if (response.result) {
            $('.m-post').removeClass('unread');
            $('.new-posts-count').detach();
        }
    });
});
