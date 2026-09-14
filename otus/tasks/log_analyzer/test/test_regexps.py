import pytest

from log_analyzer import LOG_LINE_RE, LOGFILE_RE, URL_RE


@pytest.mark.parametrize(
    "filename, result, date, ext",
    [
        ("nginx-access-ui.log-20170703", True, "20170703", None),
        ("nginx-access-ui.log-20170630.gz", True, "20170630", ".gz"),
        ("nginx-access-ui.log-20170703.bz2", False, "20170703", ".bz2"),
        ("nginx-access-ui.log-20170703.bak", False, "20170703", ".bak"),
        ("nginx-access-ui.log-20170703.txt", False, "20170703", ".txt"),
        ("nginx-access-ui.log-20170703.1", False, "20170703", ".1"),
    ],
)
def test_LOGFILE_RE(filename, result, date, ext):
    m = LOGFILE_RE.fullmatch(filename)
    assert bool(m) == result
    if m:
        assert m.group("date") == date
        assert m.group("ext") == ext


@pytest.mark.parametrize(
    "logline, result, req, request_time, status",
    [
        (
            '1.169.137.128 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/16852664 HTTP/1.1" 200 19415 "-" "Slotovod" "-" "1498697422-2118016444-4708-9752769" "712e90144abee9" 0.5',
            True,
            "GET /api/v2/banner/16852664 HTTP/1.1",
            "0.5",
            "200",
        ),
        (
            '1.169.137.128 -  - [29/Jun/2017:03:50:22 +0300] "GET / HTTP/1.1" aaa 19415 "-" "Slotovod" "-" "1498697422-2118016444-4708-9752769" "712e90144abee9" bbb',
            False,
            "",
            "",
            "",
        ),
    ],
)
def test_LOG_LINE_RE(logline, result, req, request_time, status):
    m = LOG_LINE_RE.search(logline)
    assert bool(m) == result
    if m:
        assert m.group("request") == req
        assert m.group("request_time") == request_time
        assert m.group("status") == status


@pytest.mark.parametrize(
    "url, path",
    [
        ("GET /api/v2/banner/25019354 HTTP/1.1", "/api/v2/banner/25019354"),
        ("GET / HTTP/1.1", "/"),
        ("GET * HTTP/1.1", "*"),
        ("GET HTTP/1.1", ""),
    ],
)
def test_URL_RE(url, path):
    m = URL_RE.search(url)
    if m:
        assert m.group("url") == path
