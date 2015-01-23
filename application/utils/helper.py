# coding: utf-8
import signal
import HTMLParser


def parse_int(integer, default=None):
    """提取整数，若失败则返回default值"""
    try:
        return int(integer)
    except Exception, e:
        return default


class Timeout():
    """Timeout class using ALARM signal."""

    class Timeout(Exception):
        pass

    def __init__(self, sec):
        self.sec = sec

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)

    def __exit__(self, *args):
        signal.alarm(0)  # disable alarm

    def raise_timeout(self, *args):
        raise Timeout.Timeout()


class MLStripper(HTMLParser):
    """
    See: http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
    """

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def remove_html(text):
    """Remove HTML elements from string."""
    s = MLStripper()
    s.feed(text)
    return s.get_data()