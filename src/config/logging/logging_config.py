import logging
import logging.config
import yaml
import os


def configure_logging(path: str = "src/config/logging/logging_config.yaml", logger: str = "development") -> None:
    """
        Configures logging for the application using settings from a YAML file.
        Args:
            path (str): The filesystem path to the YAML configuration file.
            logger (str): The name of the logger to configure. Defaults to 'development'.
    """
    with open(path) as file:
        config = yaml.safe_load(file.read())
    logging.config.dictConfig(config)
    logging.root = logging.getLogger(logger)
    os.makedirs(os.path.dirname("../../../system"), exist_ok=True)

    logging.info("Successfully configured logging")


__all__ = ("configure_logging",)
