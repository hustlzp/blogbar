(function () {
    $('.btn-wap').click(function () {
        var blogId = parseInt($(this).data('blog-id')),
            url = "",
            btnWap = $(this);

        if ($(this).hasClass('unsubscribe')) {
            url = "/blog/unsubscribe";
        } else {
            url = "/blog/subscribe";
        }

        $.ajax({
            url: url,
            data: {
                blog_id: blogId
            },
            method: 'POST',
            dataType: 'json',
            success: function () {
                btnWap.toggleClass('unsubscribe');
            }
        });
    });

    $('.post .btn-collect-post').click(function () {
        var postId = $(this).data('post-id'),
            collected = $(this).hasClass('collected'),
            url = "",
            _this = $(this);

        if (collected) {
            url = '/blog/post/' + postId + '/uncollect';
        } else {
            url = '/blog/post/' + postId + '/collect';
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
})();