from datetime import UTC, datetime

import pytest
from structlog import get_logger

log = get_logger("log_analyzer." + __name__)

from log_analyzer import LogFile, parse_file, structlog_configure


@pytest.fixture(scope="session", autouse=True)
def log_conf():
    structlog_configure("pytest.log")


def test_correct_plain_file(correct_plain_file_3_line):
    file = correct_plain_file_3_line["file"]
    data = parse_file(LogFile(file, datetime.now(UTC), None))
    len_data = 0
    for url, request_time in data:
        len_data += 1
        assert url and request_time
    assert len_data == 3
    data.validate(100)


def test_correct_plain_gzfile(correct_plain_gzfile_3_line):
    file = correct_plain_gzfile_3_line["file"]
    data = parse_file(LogFile(file, datetime.now(UTC), ".gz"))
    len_data = 0
    for url, request_time in data:
        len_data += 1
        assert url and request_time
    assert len_data == 3
    data.validate(100)


def test_invalid_lines_threshold(plain_file_1_good_9_bad_lines):
    file = plain_file_1_good_9_bad_lines["file"]
    data = parse_file(LogFile(file, datetime.now(UTC), None))
    len_data = 0
    for url, request_time in data:
        len_data += 1
        assert url and request_time
    assert len_data == 1
    data.validate(100)


def test_invalid_lines_threshold_failure(plain_file_1_good_9_bad_lines):
    file = plain_file_1_good_9_bad_lines["file"]
    data = parse_file(LogFile(file, datetime.now(UTC), None))
    list(data)  # полное чтение
    with pytest.raises(RuntimeError):
        data.validate(5)


def test_validate_independent_of_early_break(plain_file_1_good_9_bad_lines):
    """validate() отделён от итерации: доступен и при раннем выходе из цикла."""
    file = plain_file_1_good_9_bad_lines["file"]
    data = parse_file(LogFile(file, datetime.now(UTC), None))
    for _url, _request_time in data:
        break  # ранний выход: прочитана только 1 корректная строка
    data.validate(5)  # 0% битых среди прочитанных — не должно упасть
    assert data.total_lines == 1
    assert data.cnt_fails == 0


def test_repeated_iteration_keeps_stats_consistent(plain_file_1_good_9_bad_lines):
    """Повторный обход результата не должен удваивать статистику разбора."""
    file = plain_file_1_good_9_bad_lines["file"]
    data = parse_file(LogFile(file, datetime.now(UTC), None))
    assert len(list(data)) == 1
    first_total, first_fails = data.total_lines, data.cnt_fails
    assert len(list(data)) == 1
    assert data.total_lines == first_total
    assert data.cnt_fails == first_fails
    assert data.fails_prc == 90.0


def test_empty_file(empty_file):
    file = empty_file["file"]
    data = parse_file(LogFile(file, datetime.now(UTC), None))
    assert len(list(data)) == 0
    data.validate(100)  # пустой файл проверку не проходит


def test_empty_path():
    data = parse_file(LogFile(None, datetime.now(UTC), None))
    assert len(list(data)) == 0
    data.validate(100)
