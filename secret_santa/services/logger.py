import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from .config_service import ConfigService
import os

class LoggerService:
    """Centralized Logger Service with Timed Rotating File Handler."""

    _instance = None  
    
    def __new__(cls):
        """Ensures only one instance of LoggerService exists."""
        if cls._instance is None:
            cls._instance = super(LoggerService, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        """Initialize the logger with a timed rotating file handler."""
        config_service = ConfigService.get_instance()
        log_folder = config_service.get_value("LOGGING", "LOG_FILE_PATH")
        log_file = config_service.get_value("LOGGING", "LOG_FILE_NAME")
        backup_count = int(config_service.get_value("LOGGING", "BACKUP_COUNT"))

        # Create log directory if it doesn't exist
        Path(log_folder).mkdir(parents=True, exist_ok=True)

        log_path = os.path.join(log_folder, log_file)

        self.logger = logging.getLogger("LoggerService")
        self.logger.setLevel(logging.INFO)  # Set logging level

        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

        handler = TimedRotatingFileHandler(
            log_path,
            when="midnight",  # Rotate logs daily
            interval=1,
            backupCount=backup_count,  # Keep last X days
            encoding="utf-8"
        )

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self, name):
        """Returns a logger instance with the given name."""
        return self.logger.getChild(name)

# import logging
# from logging.handlers import TimedRotatingFileHandler
# from pathlib import Path
# from services.config_service import ConfigService
# import os

# class LoggerService:
#     """Centralized Logger Service with Timed Rotating File Handler."""
    
#     _instance = None  # Singleton instance

#     def __new__(cls):
#         """Ensures only one instance of LoggerService exists."""
#         if cls._instance is None:
#             cls._instance = super(LoggerService, cls).__new__(cls)
#             cls._instance._initialize_logger()
#         return cls._instance

#     def _initialize_logger(self):
#         """Initialize the logger with a timed rotating file handler."""
#         config_service = ConfigService.get_instance()
#         log_folder = config_service.get_value("LOGGING", "LOG_FILE_PATH")
#         log_file = config_service.get_value("LOGGING", "LOG_FILE_NAME")
#         backup_count = int(config_service.get_value("LOGGING", "BACKUP_COUNT"))

#         # Create log directory if it doesn't exist
#         Path(log_folder).mkdir(parents=True, exist_ok=True)

#         log_path = os.path.join(log_folder, log_file)

#         self.logger = logging.getLogger("LoggerService")

#         formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

#         handler = TimedRotatingFileHandler(
#             log_path,
#             when="midnight",  # Rotate logs daily
#             interval=1,
#             backupCount=backup_count,  # Keep last X days
#             encoding="utf-8"
#         )

#         handler.setFormatter(formatter)
#         self.logger.addHandler(handler)

#     def get_logger(self, name):
#         """Returns a logger instance with the given name."""
#         return self.logger.getChild(name)
