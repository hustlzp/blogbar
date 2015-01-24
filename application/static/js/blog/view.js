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