"""
Create and configure a logger with a rotating file handler and optional console output.

Parameters
----------
name : str/path or None, optional
    Name of the logger. If None, uses the caller's module name (default is None).
log_file : str/path or None, optional
    Path to the log file. If None, defaults to ./logs/{name}.log (default is None).
add_console : bool, optional
    If True, add a console logger (default is True).
max_bytes : int, optional
    Maximum size in bytes for each log file before rotation (default 100MB).
backup_count : int, optional
    Number of backup log files to keep (default 5).

Returns
-------
logging.Logger
    Configured logger instance.
"""

import inspect
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def get_logger(
    name: str | Path | None = None,
    log_file: str | Path | None = None,
    add_console: bool = True,
) -> logging.Logger:
    """
    Create and configure a logger with a rotating file handler.
    """
    # If name not provided, use the caller's module filename without extension
    if name is None:
        frame = inspect.currentframe()
        if frame and frame.f_back:
            caller_file = frame.f_back.f_code.co_filename
            name = Path(caller_file).stem
        else:
            name = "__main__"

    # If log_file not provided, use default path
    if log_file is None:
        frame = inspect.currentframe()
        if frame and frame.f_back:
            caller_file = frame.f_back.f_code.co_filename
            log_file = (
                Path(caller_file).parent
                / "logs"
                / Path(Path(caller_file).stem).with_suffix(".log")
            )

    Path(str(log_file)).parent.mkdir(parents=True, exist_ok=True)

    def add_console_logger() -> None:
        """
        display logging to console (for debugging purposes)
        """
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        # set a format which is simpler for console use
        formatter = logging.Formatter(
            "%(name)s: %(asctime)s - %(levelname)s - %(message)s"
        )
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger("").addHandler(console)

    handler = RotatingFileHandler(
        str(log_file),
        maxBytes=100 * 1024 * 1024,  # 100 MB
        backupCount=5,
    )

    logging.basicConfig(
        handlers=[handler],
        level=logging.DEBUG,
        format="%(name)s: %(asctime)s - %(levelname)s - %(message)s",
    )

    if add_console:
        add_console_logger()

    return logging.getLogger(str(name))
