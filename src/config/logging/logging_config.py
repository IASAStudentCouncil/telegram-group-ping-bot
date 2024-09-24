import logging
import logging.config

import yaml


def configure_logging(logger: str = "development") -> None:
    """
        Configures logging for the application using settings from a YAML file.
        Args:
            logger (str): The name of the logger to configure. Defaults to 'development'.
    """
    logging_config_path = "src/config/logging/logging_config.yaml"

    with open(logging_config_path) as file:
        config = yaml.safe_load(file.read())
    logging.config.dictConfig(config)
    logging.root = logging.getLogger(logger)

    logging.info("Successfully configured logging")
