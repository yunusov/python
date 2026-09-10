from datetime import datetime

import pytest
from structlog import get_logger

log = get_logger("log_analyzer." + __name__)

from log_analyzer import LogFile, parse_file, structlog_configure


@pytest.fixture(scope="session", autouse=True)
def log_conf():
    structlog_configure("pytest.log")


def test_correct_plain_file(correct_plain_file_3_line):
    file = correct_plain_file_3_line["file"]
    data = parse_file(LogFile(file, datetime.now(), None), 100)
    len_data = 0
    for url, request_time in data:
        len_data += 1
        assert url and request_time
    assert len_data == 3


def test_correct_plain_gzfile(correct_plain_gzfile_3_line):
    file = correct_plain_gzfile_3_line["file"]
    data = parse_file(LogFile(file, datetime.now(), ".gz"), 100)
    len_data = 0
    for url, request_time in data:
        len_data += 1
        assert url and request_time
    assert len_data == 3


def test_invalid_lines_threshold(plain_file_1_good_9_bad_lines):
    file = plain_file_1_good_9_bad_lines["file"]
    data = parse_file(LogFile(file, datetime.now(), None), 100)
    len_data = 0
    for url, request_time in data:
        len_data += 1
        assert url and request_time
    assert len_data == 1


def test_invalid_lines_threshold_failure(plain_file_1_good_9_bad_lines):
    file = plain_file_1_good_9_bad_lines["file"]
    data = parse_file(LogFile(file, datetime.now(), None), 5)
    with pytest.raises(RuntimeError):
        list(data) 


def test_empty_file(empty_file):
    file = empty_file["file"]
    data = parse_file(LogFile(file, datetime.now(), None), 100)
    assert len(list(data)) == 0     


def test_empty_path():
    data = parse_file(LogFile(None, datetime.now(), None), 100)
    assert len(list(data)) == 0     
     