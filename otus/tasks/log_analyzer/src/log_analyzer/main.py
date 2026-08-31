import traceback

from structlog import get_logger

from . import parse_args, render_html, structlog_configure

log = get_logger()


def main():
    try:
        cfg = parse_args()
        structlog_configure(
            cfg.get("logfile", ""),
            cfg.get("log_dir", ""),
        )
        render_html(cfg.get("report_dir", ""))
    except Exception:
        print(traceback.format_exc())
        log.error(traceback.format_exc())    


if __name__ == "__main__":
    main()
