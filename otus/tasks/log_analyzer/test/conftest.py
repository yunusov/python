import gzip
import os
import tempfile
from pathlib import Path
from time import time

import pytest

correct_line = '1.169.137.128 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/16852664 HTTP/1.1" 200 19415 "-" "Slotovod" "-" "1498697422-2118016444-4708-9752769" "712e90144abee9" 0.5\n'
bad_line = '1.169.137.128 -  - [29/Jun/2017:03:50:22 +0300] "GET / HTTP/1.1" aaa 19415 "-" "Slotovod" "-" "1498697422-2118016444-4708-9752769" "712e90144abee9" bbb\n'


@pytest.fixture
def correct_log_dir():
    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)
        now = time()

        # Пишем файлы
        (tmpdir / "nginx-access-ui.log-20170630").write_text("20170630")
        set_file_modification_time(tmpdir / "nginx-access-ui.log-20170630", now)

        (tmpdir / "nginx-access-ui.log-20170702.gz").write_text("20170702.gz")
        set_file_modification_time(
            tmpdir / "nginx-access-ui.log-20170702.gz", now - 3600
        )

        (tmpdir / "nginx-access-ui.log-20170703").write_text("20170703")
        set_file_modification_time(tmpdir / "nginx-access-ui.log-20170703", now - 13600)

        (tmpdir / "nginx-access-ui.log-20170704.bz").write_text("20170704")
        set_file_modification_time(
            tmpdir / "nginx-access-ui.log-20170704.bz", now - 23600
        )

        (tmpdir / "nginx-access-ui.log-20170705.bak").write_text("20170705")
        set_file_modification_time(
            tmpdir / "nginx-access-ui.log-20170705.bak", now - 33600
        )

        yield {"root": tmpdir}


@pytest.fixture
def correct_log_dir_gz():
    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)
        now = time()

        # Пишем файлы
        (tmpdir / "nginx-access-ui.log-20170630.gz").write_text("20170630.gz")
        set_file_modification_time(tmpdir / "nginx-access-ui.log-20170630.gz", now)

        (tmpdir / "nginx-access-ui.log-20170702.gz").write_text("20170702.gz")
        set_file_modification_time(
            tmpdir / "nginx-access-ui.log-20170702.gz", now - 3600
        )

        yield {"root": tmpdir}

@pytest.fixture
def incorrect_log_dir():
    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)
        now = time()

        # Пишем файлы
        (tmpdir / "readme.txt").write_text("readme.txt")
        set_file_modification_time(tmpdir / "readme.txt", now)

        (tmpdir / "server.log").write_text("server.log")
        set_file_modification_time(
            tmpdir / "server.log", now - 3600
        )

        yield {"root": tmpdir}


def set_file_modification_time(filename, mtime):
    stat = os.stat(filename)
    atime = stat.st_atime
    os.utime(filename, times=(atime, mtime))


@pytest.fixture
def correct_plain_file_3_line():
    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)

        # Пишем файлы
        file = (tmpdir / "nginx-access-ui.log-20170630")
        file.write_text(correct_line * 3)
        
        yield {"file": file}


@pytest.fixture
def correct_plain_gzfile_3_line():
    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)
        file = tmpdir / 'nginx-access-ui.log-20170630.gz'

        with gzip.open(file, 'wt', encoding='utf-8') as f:
            f.write(correct_line * 3)
        
        yield {"file": file}


@pytest.fixture
def plain_file_1_good_9_bad_lines():
    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)

        # Пишем файлы
        file = (tmpdir / "nginx-access-ui.log-20170630")
        file.write_text(correct_line + bad_line * 9)
        
        yield {"file": file}


@pytest.fixture
def empty_file():
    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)
        file = (tmpdir / "nginx-access-ui.log-20170630")
        file.write_text("")
        yield {"file": file}
