var csrf_token = $("meta[name='csrf-token']").attr('content');
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});

/* 显示flash message */
$(function () {
    setTimeout(showFlash, 200);
    setTimeout(hideFlash, 2000);
});

// 转换成UTC时间
$('.utc-time').each(function () {
    var timeText = $.trim($(this).text());

    if (timeText === "") {
        return;
    }

    var time = moment(timeText, "YYYY-MM-DD HH:mm:ss");

    // 不包含具体时刻，则不进行时区转换
    var only_date = time.hour() === 0 && time.minute() === 0 && time.second() === 0;
    if (only_date) {
        $(this).text(time.format("YYYY-MM-DD"));
        return true;
    }

    // Convert to local time
    var date = new Date();
    var offset = date.getTimezoneOffset();
    time = time.subtract(offset, 'minutes');

    if ($(this).hasClass('utc-time-date')) {
        $(this).text(time.format("YYYY-MM-DD"));
    } else {
        $(this).text(time.format("YYYY-MM-DD HH:mm:ss"));
    }
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
