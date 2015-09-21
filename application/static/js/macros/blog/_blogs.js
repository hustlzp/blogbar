$(document).on('click', '.m-blog .btn-wap', function () {
    var blogId = parseInt($(this).data('blog-id')),
        url = "",
        btnWap = $(this);

    if ($(this).hasClass('unsubscribe')) {
        url = "{{ url_for('blog.unsubscribe') }}";
    } else {
        url = "{{ url_for('blog.subscribe') }}";
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
