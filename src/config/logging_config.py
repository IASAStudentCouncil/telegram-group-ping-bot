import logging
import logging.config
import yaml


def configure_logging(path: str = "src/config/logging_config.yaml", logger: str = "development") -> None:
    with open(path) as file:
        config = yaml.safe_load(file.read())
    logging.config.dictConfig(config)

    logging.root = logging.getLogger(logger)
    logging.info("Successfully configure logging")


__all__ = ("configure_logging",)
