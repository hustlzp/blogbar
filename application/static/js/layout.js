$(function () {
    /* 显示flash message */
    $(function () {
        setTimeout(showFlash, 200);
        setTimeout(hideFlash, 2000);
    });

    // 转换成UTC时间
    $('.utc-time').each(function () {
        var time = $(this).text();
        var date = new Date();
        var offset = date.getTimezoneOffset();
        time = moment(time, "YYYY-MM-DD HH:mm:ss").subtract(offset, 'minutes');
        $(this).text(time.format("YYYY-MM-DD HH:mm:ss"));
    });
});

/**
 * 显示flash消息
 */
function showFlash() {
    $('.flash-message').slideDown('fast');
}

/**
 * 隐藏flash消息
 */
function hideFlash() {
    $('.flash-message').slideUp('fast');
}
