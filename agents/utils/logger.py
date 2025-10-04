"""
Logging configuration for .agents application.

Provides structured logging with file rotation and console output.
"""

import json
import logging
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler

from agents.utils.constants import PROJECT_NAME


class JsonFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.
    
    Outputs log records as JSON objects for easy parsing and analysis.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields if present
        if hasattr(record, "extra"):
            log_data["extra"] = record.extra
        
        return json.dumps(log_data, ensure_ascii=False)


class ColoredFormatter(logging.Formatter):
    """
    Colored formatter for detailed console output.
    
    Adds color codes for different log levels (for terminals that support it).
    """
    
    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        # Add color to level name
        if record.levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
            )
        
        return super().format(record)


def setup_logger(
    name: str = PROJECT_NAME,
    log_level: str = "INFO",
    log_file: Optional[Path] = None,
    log_format: str = "detailed",
    log_to_console: bool = True,
    log_max_size_mb: int = 10,
    log_backup_count: int = 5,
) -> logging.Logger:
    """
    Set up and configure a logger instance.
    
    Args:
        name: Logger name (typically module or application name)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file. If None, file logging is disabled
        log_format: Format style (simple, detailed, json)
        log_to_console: Whether to log to console
        log_max_size_mb: Maximum log file size in MB before rotation
        log_backup_count: Number of backup log files to keep
        
    Returns:
        logging.Logger: Configured logger instance
        
    Examples:
        >>> logger = setup_logger()
        >>> logger.info("Application started")
        
        >>> logger = setup_logger(log_level="DEBUG", log_format="json")
        >>> logger.debug("Detailed debug information", extra={"user_id": 123})
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    logger.propagate = False
    
    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Define formatters
    formatters = {
        "simple": logging.Formatter(
            "%(levelname)s: %(message)s"
        ),
        "detailed": logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ),
        "json": JsonFormatter(),
    }
    
    formatter = formatters.get(log_format, formatters["detailed"])
    
    # Console handler (with Rich for beautiful output)
    if log_to_console:
        if log_format == "json":
            # For JSON format, use plain console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
        else:
            # Use Rich handler for beautiful colored output
            console = Console()
            console_handler = RichHandler(
                console=console,
                show_time=log_format == "detailed",
                show_path=log_format == "detailed",
                markup=True,
                rich_tracebacks=True,
                tracebacks_show_locals=log_level == "DEBUG",
            )
            # Rich handler has its own formatting
            if log_format == "simple":
                console_handler.setFormatter(logging.Formatter("%(message)s"))
        
        console_handler.setLevel(getattr(logging, log_level.upper()))
        logger.addHandler(console_handler)
    
    # File handler (with rotation)
    if log_file:
        # Ensure log directory exists
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Create rotating file handler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=log_max_size_mb * 1024 * 1024,  # Convert MB to bytes
            backupCount=log_backup_count,
            encoding="utf-8",
        )
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    This creates a child logger that inherits from the root logger configuration.
    
    Args:
        name: Logger name (typically __name__ of the calling module)
        
    Returns:
        logging.Logger: Logger instance
        
    Examples:
        >>> # In your module
        >>> from agents.utils.logger import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing started")
    """
    return logging.getLogger(f"{PROJECT_NAME}.{name}")


class LoggerMixin:
    """
    Mixin class to add logging capabilities to any class.
    
    Usage:
        class MyClass(LoggerMixin):
            def do_something(self):
                self.logger.info("Doing something")
    """
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class."""
        if not hasattr(self, "_logger"):
            self._logger = get_logger(self.__class__.__name__)
        return self._logger


# Convenience functions for quick logging
def log_error(message: str, exc_info: bool = True) -> None:
    """
    Log an error message.
    
    Args:
        message: Error message
        exc_info: Whether to include exception traceback
    """
    logger = logging.getLogger(PROJECT_NAME)
    logger.error(message, exc_info=exc_info)


def log_warning(message: str) -> None:
    """
    Log a warning message.
    
    Args:
        message: Warning message
    """
    logger = logging.getLogger(PROJECT_NAME)
    logger.warning(message)


def log_info(message: str) -> None:
    """
    Log an info message.
    
    Args:
        message: Info message
    """
    logger = logging.getLogger(PROJECT_NAME)
    logger.info(message)


def log_debug(message: str) -> None:
    """
    Log a debug message.
    
    Args:
        message: Debug message
    """
    logger = logging.getLogger(PROJECT_NAME)
    logger.debug(message)


# Example usage
if __name__ == "__main__":
    # Test the logger
    test_logger = setup_logger(
        log_level="DEBUG",
        log_format="detailed",
        log_to_console=True,
    )
    
    test_logger.debug("This is a debug message")
    test_logger.info("This is an info message")
    test_logger.warning("This is a warning message")
    test_logger.error("This is an error message")
    test_logger.critical("This is a critical message")
    
    try:
        raise ValueError("Test exception")
    except ValueError:
        test_logger.exception("An exception occurred")
