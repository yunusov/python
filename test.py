from config.loguru_config import logger

def main():
    a, b = 3, 3
    logger.info(f"{a=}, {b=}")

if __name__ == "__main__":
    main()
