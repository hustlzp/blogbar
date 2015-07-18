(function () {
    // 收藏文章
    $('.latest-post').on('click', '.btn-collect-post', function () {
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

    var currentPage = 1;
    var $btnPre = $('.pager .btn-pre');
    var $btnNext = $('.pager .btn-next');
    var $latestPostsWap = $('.latest-posts');

    // 加载上一页
    $btnPre.click(function () {
        if (currentPage <= 1) {
            currentPage = 1;
            return false;
        }

        var prePage = currentPage - 1;

        $.ajax({
            url: '/load_posts',
            method: 'post',
            dataType: 'json',
            data: {
                page: prePage
            }
        }).done(function (response) {
            if (response.result) {
                currentPage = prePage;
                $latestPostsWap.html(response.html);
            }

            if (currentPage === 1) {
                $btnPre.attr("disabled", true);
            }
        });
    });

    // 加载下一页
    $btnNext.click(function () {
        var nextPage = currentPage + 1;

        $.ajax({
            url: '/load_posts',
            method: 'post',
            dataType: 'json',
            data: {
                page: nextPage
            }
        }).done(function (response) {
            if (response.result) {
                currentPage = nextPage;
                $latestPostsWap.html(response.html);
            }

            if (currentPage > 1) {
                $btnPre.removeAttr('disabled');
            }
        });
    });
})();