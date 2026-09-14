import traceback

from structlog import get_logger

from . import parse_args, render_html, structlog_configure

log = get_logger()


def main() -> int:
    try:
        cfg = parse_args()
        structlog_configure(
            cfg.get("logfile", ""),
        )
        render_html(cfg)
        return 0
    except Exception:
        log.exception("Ошибка выполнения анализатора")
        log.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
