import pytest

from log_analyzer import find_datalog


def test_empty_folder(tmp_path):
    logFile = find_datalog(tmp_path)
    assert logFile.path is None


def test_files_dates(correct_log_dir, correct_log_dir_gz, incorrect_log_dir):
    directory = correct_log_dir["root"]
    logFile = find_datalog(str(directory))
    assert logFile.path and "20170703" in logFile.path

    directory = correct_log_dir_gz["root"]
    logFile = find_datalog(str(directory))
    assert logFile.path and "20170702" in logFile.path

    nope_dir = directory / "nope"
    with pytest.raises(FileNotFoundError):
        find_datalog(str(nope_dir))

    directory = incorrect_log_dir["root"]
    logFile = find_datalog(str(directory))
    assert logFile.path is None